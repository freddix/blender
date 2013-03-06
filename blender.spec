Summary:	3D content creation suite
Name:		blender
Version:	2.66
Release:	0.4
License:	GPL v2
Group:		X11/Applications
Source0:	http://download.blender.org/source/%{name}-%{version}.tar.gz
# Source0-md5:	159aedda89693321c5055819fa8e91cf
Patch0:		%{name}-scripts.patch
Patch1:		%{name}-locale.patch
Patch2:		%{name}-path.patch
Patch3:		%{name}-font-fixes.patch
Patch4:		%{name}-fix-format.patch
Patch5:		%{name}-sys-path.patch
Patch6:		%{name}-dbgedit.patch
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	fftw3-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freealut-devel
BuildRequires:	freetype-devel
BuildRequires:	glew-devel
BuildRequires:	jack-devel
BuildRequires:	libav-devel
BuildRequires:	libgomp-devel
BuildRequires:	libpng-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libtiff-devel
BuildRequires:	pkg-config
BuildRequires:	python3-devel
BuildRequires:	xorg-libX11-devel
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
%pyrequires_eq	python3-modules
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
Requires:	fonts-TTF-droid
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Blender is an integrated 3d suite for modelling, animation, rendering,
post-production, interactive creation and playback (games). Blender has its
own particular user interface, which is implemented entirely in OpenGL and
designed with speed in mind. Python bindings are available for scripting;
import/export features for popular file formats like 3D Studio and Wavefront
Obj are implemented as scripts by the community. Stills, animations, models
for games or other third party engines and interactive content in the form of
a standalone binary are common products of Blender use.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
mkdir build
cd build
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF			\
	-DCMAKE_SKIP_RPATH=ON			\
	-DCMAKE_VERBOSE_MAKEFILE=ON		\
	-DPYTHON_VERSION:STRING=3.3		\
	-DWITH_BUILTIN_GLEW=OFF			\
	-DWITH_CODEC_FFMPEG=ON			\
	-DWITH_CODEC_SNDFILE:BOOL=ON		\
	-DWITH_CODEC_SNDFILE=ON			\
	-DWITH_CYCLES=OFF			\
	-DWITH_FFTW3=ON				\
	-DWITH_FONTCONFIG=ON			\
	-DWITH_IMAGE_OPENJPEG:BOOL=ON		\
	-DWITH_INSTALL_PORTABLE=OFF		\
	-DWITH_JACK=ON				\
	-DWITH_MOD_OCEANSIM=ON			\
	-DWITH_PLAYER=ON			\
	-DWITH_PYTHON:BOOL=ON			\
	-DWITH_PYTHON_INSTALL:BOOL=OFF		\
	-DWITH_PYTHON_SAFETY=ON
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install -C build \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/es_ES

%find_lang %{name}

find $RPM_BUILD_ROOT -type f -name "*.py" -print | \
	xargs sed -i "s|/usr/bin/python|/usr/bin/python3|g"

%py3_comp $RPM_BUILD_ROOT%{_datadir}/blender
%py3_ocomp $RPM_BUILD_ROOT%{_datadir}/blender

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/blender
%attr(755,root,root) %{_bindir}/blender-thumbnailer.py
%attr(755,root,root) %{_bindir}/blenderplayer
%{_datadir}/blender
%{_desktopdir}/blender.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/*/apps/*.svg
%{_mandir}/man1/blender.1*

