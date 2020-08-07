@echo off
:#*****************************************************************************
:#                                                                            *
:#  Filename:	    make.bat						      *
:#                                                                            *
:#  Description:    Build DOS and Windows targets			      *
:#                                                                            *
:#  Notes:	    Proxy script for %STINCLUDE%\make.bat.		      *
:#                                                                            *
:#                  If any change is needed, put it in %STINCLUDE%\make.bat.  *
:#                                                                            *
:#  History:                                                                  *
:#   2016-10-10 JFL jf.larvoire@hpe.com created this file.		      *
:#   2016-12-15 JFL Search for the real make.bat in [.|..|../..]\include.     *
:#                                                                            *
:#        � Copyright 2016 Hewlett Packard Enterprise Development LP          *
:# Licensed under the Apache 2.0 license  www.apache.org/licenses/LICENSE-2.0 *
:#*****************************************************************************

:# Get the full pathname of the STINCLUDE library directory
if defined STINCLUDE if not exist "%STINCLUDE%\make.bat" set "STINCLUDE=" &:# Allow overriding with another alias name, but ignore invalid overrides
for %%p in (. .. ..\..) do if not defined STINCLUDE if exist %%p\include\make.bat ( :# Default: Search it the current directory, and 2 levels above.
  for /f "delims=" %%d in ('"pushd %%p\include & cd & popd"') do SET "STINCLUDE=%%d"
)
if not defined STINCLUDE ( :# Try getting the copy in the master environment
  for /f "tokens=3" %%v in ('reg query "HKCU\Environment" /v STINCLUDE 2^>NUL') do set "STINCLUDE=%%v"
)

if not exist %STINCLUDE%\make.bat (
  >&2 echo %0 Error: Cannot find SysToolsLib's global C include directory. Please define variable STINCLUDE.
  exit /b 1
)

if [%1]==[-d] echo "%STINCLUDE%\make.bat" %*
"%STINCLUDE%\make.bat" %*
