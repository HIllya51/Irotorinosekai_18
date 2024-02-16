#include <windows.h>
#include "CMem.h"
#include "ImageEx.h"
#include "WinFile.h"
#include "TLGDecoder.h"
#include <string>
#include<gdiplus.h>
#pragma comment(lib, "ntdll.lib")
#pragma comment(lib, "gdiplus.lib")
using std::wstring;
using namespace Gdiplus;
int GetEncoderClsid(const WCHAR* format, CLSID* pClsid)
{
	UINT  num = 0;          // number of image encoders
	UINT  size = 0;         // size of the image encoder array in bytes

	ImageCodecInfo* pImageCodecInfo = NULL;

	GetImageEncodersSize(&num, &size);
	if (size == 0)
		return -1;  // Failure

	pImageCodecInfo = (ImageCodecInfo*)(malloc(size));
	if (pImageCodecInfo == NULL)
		return -1;  // Failure

	GetImageEncoders(num, size, pImageCodecInfo);

	for (UINT j = 0; j < num; ++j)
	{
		if (wcscmp(pImageCodecInfo[j].MimeType, format) == 0)
		{
			*pClsid = pImageCodecInfo[j].Clsid;
			free(pImageCodecInfo);
			return j;  // Success
		}
	}

	free(pImageCodecInfo);
	return -1;  // Failure
}
void castbmp2png(const wchar_t* fname, Bitmap* bitmap) {

	CLSID   encoderClsid;
	Status  stat;
	/* Image* image = Bitmap::FromBITMAPINFO(bitMapInfo, bitMapData);
	 Bitmap::Bitmap(0).Save(); */
	 // Get the CLSID of the PNG encoder.
	GetEncoderClsid(L"image/png", &encoderClsid);

	stat = bitmap->Save(fname, &encoderClsid, NULL);

}
int wmain(int argc, WCHAR** argv)
{
	if (argc != 2)
	{
		return 0;
	}
	WinFile File;
	if (File.Open(argv[1], WinFile::FileRead) != S_OK)
	{
		return 0;
	}
	BYTE Magic[6] = {0};
	File.Read((PBYTE)&Magic[0], sizeof(Magic));
	File.Seek(0, FILE_BEGIN);
	ULONG Size = File.GetSize32();
	PBYTE Buffer = (PBYTE)CMem::Alloc(Size);
	File.Read(Buffer, Size);
	PBYTE OutBuffer = nullptr;
	ULONG OutSize = 0;
	if (RtlCompareMemory(Magic, KRKR2_TLG5_MAGIC, 6) == 6)
	{
		if (!DecodeTLG5(Buffer, Size, (PVOID*)&OutBuffer, &OutSize))
		{
			MessageBoxW(NULL, L"Failed to decode tlg5.0 file", L"TLGTest", MB_OK);
			CMem::Free(Buffer);
			File.Release();
			return 0;
		}
	}
	else if (RtlCompareMemory(Magic, KRKR2_TLG6_MAGIC, 6) == 6)
	{
		if (!DecodeTLG6(Buffer, Size, (PVOID*)&OutBuffer, &OutSize))
		{
			MessageBoxW(NULL, L"Failed to decode tlg6.0 file", L"TLGTest", MB_OK);
			CMem::Free(Buffer);
			File.Release();
			return 0;
		}
	}//KRKR2_TLG0_MAGIC
	else if (RtlCompareMemory(Magic, KRKR2_TLG0_MAGIC, 6) == 6)
	{
		//Dummy Header?
		//I hope this header will never used for extraction in the future.
		if (RtlCompareMemory(Buffer + 0xF, KRKR2_TLG5_MAGIC, 6) == 6)
		{
			if (!DecodeTLG5(Buffer + 0xF, Size - 0xF, (PVOID*)&OutBuffer, &OutSize))
			{
				MessageBoxW(NULL, L"Failed to decode tlg6.0 file", L"TLGTest", MB_OK);
				CMem::Free(Buffer);
				File.Release();
				return 0;
			}
		}
		else
		{
			if (!DecodeTLG6(Buffer + 0xF, Size - 0xF, (PVOID*)&OutBuffer, &OutSize))
			{
				MessageBoxW(NULL, L"Failed to decode tlg6.0 file", L"TLGTest", MB_OK);
				CMem::Free(Buffer);
				File.Release();
				return 0;
			}
		}
	}
	else
	{
		MessageBoxW(NULL, L"Unsupported format", L"TLGTest", MB_OK);
		return 0;
	}
	File.Release();
	if (OutSize)
	{
		/*wstring FileName(argv[1]);
		FileName += L".bmp";
		WinFile OutFile;
		if (OutFile.Open(FileName.c_str(), WinFile::FileWrite) != S_OK)
		{
			MessageBoxW(NULL, L"Cannot create a handle for output file!", L"TLGTest", MB_OK);
			return 0;
		}
		OutFile.Write(OutBuffer, OutSize);
		OutFile.Release();*/


		IStream* pStream = nullptr;
		CreateStreamOnHGlobal(NULL, TRUE, &pStream);
		pStream->Write(OutBuffer, OutSize, NULL);
		GdiplusStartupInput gdiplusStartupInput;
		ULONG_PTR gdiplusToken;
		GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
		auto bit = Bitmap::FromStream(pStream);
		castbmp2png((std::wstring(argv[1]) + L".png").c_str(), bit);
	}
	
	return 0;
}

