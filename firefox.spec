%global system_nss        1
%global system_sqlite     0
%global system_ffi        1
%global system_cairo      0
%global system_libvpx     1
%global system_libicu     0
%global hardened_build    1
%global system_jpeg       1

%if 0%{?fedora} > 29
%global wayland_backend_default 1
%else
%global wayland_backend_default 0
%endif

%if 0%{?fedora} < 29
%global use_bundled_cbindgen    1
%endif

# Big endian platforms
%ifarch ppc64 s390x
%global big_endian        1
%endif

%ifarch %{ix86} x86_64
%global run_tests         0
%else
%global run_tests         0
%endif

%bcond_without debug_build
%if %{with debug_build}
%else
%global debug_build       1
%else
%global debug_build       0
%endif

%global disable_elfhack   0
%if 0%{?fedora} > 28
%global disable_elfhack   1
%endif

%global default_bookmarks_file  %{_datadir}/bookmarks/default-bookmarks.html
%global firefox_app_id  \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
# Minimal required versions
%global cairo_version 1.13.1
%global freetype_version 2.1.9
%global libnotify_version 0.7.0
%if %{?system_libvpx}
%global libvpx_version 1.4.0
%endif

%if %{?system_nss}
%global nspr_version 4.19
# NSS/NSPR quite often ends in build override, so as requirement the version
# we're building against could bring us some broken dependencies from time to time.
#%global nspr_build_version %(pkg-config --silence-errors --modversion nspr 2>/dev/null || echo 65536)
%global nspr_build_version %{nspr_version}
%global nss_version 3.37.3
#%global nss_build_version %(pkg-config --silence-errors --modversion nss 2>/dev/null || echo 65536)
%global nss_build_version %{nss_version}
%endif

%if %{?system_sqlite}
%global sqlite_version 3.8.4.2
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

%global mozappdir     %{_libdir}/%{name}
%global mozappdirdev  %{_libdir}/%{name}-devel-%{version}
%global langpackdir   %{mozappdir}/langpacks
%global tarballdir    firefox-%{version}

%global official_branding       1

%bcond_without langpacks

%global enable_mozilla_crashreporter       0
%if !%{debug_build}
%ifarch %{ix86} x86_64
%global enable_mozilla_crashreporter       1
%endif
%endif

Summary:        Mozilla Firefox Web browser
Name:           firefox
Version:        63.0.1
Release:        2%{?pre_tag}%{?dist}
URL:            https://www.mozilla.org/firefox/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Source0:        https://archive.mozilla.org/pub/firefox/releases/%{version}%{?pre_version}/source/firefox-%{version}%{?pre_version}.source.tar.xz
%if %{with langpacks}
Source1:        firefox-langpacks-%{version}%{?pre_version}-20181101.tar.xz
%endif
Source2:        cbindgen-vendor.tar.xz
Source10:       firefox-mozconfig
Source12:       firefox-redhat-default-prefs.js
Source20:       firefox.desktop
Source21:       firefox.sh.in
Source23:       firefox.1
Source24:       mozilla-api-key
Source25:       firefox-symbolic.svg
Source26:       distribution.ini
Source27:       google-api-key
Source28:       firefox-wayland.sh.in
Source29:       firefox-wayland.desktop
Source30:       firefox-x11.sh.in
Source31:       firefox-x11.desktop

# Build patches
Patch3:         mozilla-build-arm.patch
Patch25:        rhbz-1219542-s390-build.patch
Patch26:        build-icu-big-endian.patch
Patch27:        mozilla-1335250.patch
Patch32:        build-rust-ppc64le.patch
Patch35:        build-ppc-jit.patch
# Always feel lucky for unsupported platforms:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1347128
Patch37:        build-jit-atomic-always-lucky.patch
# Fixing missing cacheFlush when JS_CODEGEN_NONE is used (s390x)
Patch38:        build-cacheFlush-missing.patch
Patch40:        build-aarch64-skia.patch
Patch41:        build-disable-elfhack.patch
Patch42:        prio-nss-build.patch
Patch43:        mozilla-1500366.patch
Patch44:        mozilla-1494037.patch

# Fedora specific patches
Patch215:        firefox-enable-addons.patch
Patch219:        rhbz-1173156.patch
Patch221:        firefox-fedora-ua.patch
Patch224:        mozilla-1170092.patch
#ARM run-time patch
Patch226:        rhbz-1354671.patch

# Upstream patches
Patch402:        mozilla-1196777.patch
Patch406:        mozilla-256180.patch
Patch410:        mozilla-1321521.patch
Patch411:        mozilla-1321521-2.patch
Patch412:        mozilla-1337988.patch
Patch413:        mozilla-1353817.patch
Patch414:        mozilla-1435212-ffmpeg-4.0.patch
Patch415:        Bug-1238661---fix-mozillaSignalTrampoline-to-work-.patch
Patch416:        mozilla-1424422.patch
Patch417:        bug1375074-save-restore-x28.patch
Patch421:        mozilla-1447775.patch

# Wayland specific upstream patches
Patch573:        mozilla-1415078.patch
Patch574:        firefox-pipewire.patch
Patch581:        mozilla-1493081.patch

# Debian patches
Patch500:        mozilla-440908.patch

%if %{?system_nss}
BuildRequires:  pkgconfig(nspr) >= %{nspr_version}
BuildRequires:  pkgconfig(nss) >= %{nss_version}
BuildRequires:  nss-static >= %{nss_version}
%endif
%if %{?system_cairo}
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
%endif
BuildRequires:  pkgconfig(libpng)
%if %{?system_jpeg}
BuildRequires:  libjpeg-devel
%endif
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libIDL-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(libstartup-notification-1.0)
BuildRequires:  pkgconfig(libnotify) >= %{libnotify_version}
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  dbus-glib-devel
%if %{?system_libvpx}
BuildRequires:  libvpx-devel >= %{libvpx_version}
%endif
BuildRequires:  autoconf213
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  yasm
BuildRequires:  llvm
BuildRequires:  llvm-devel
BuildRequires:  clang
BuildRequires:  clang-libs
%if 0%{?fedora} > 27
BuildRequires:  pipewire-devel
%endif

%if !0%{?use_bundled_cbindgen}
BuildRequires:  cbindgen
%endif

BuildRequires:  nodejs

Requires:       mozilla-filesystem
Requires:       p11-kit-trust
%if %{?system_nss}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif
BuildRequires:  python2-devel
Requires:       u2f-hidraw-policy

%if 0%{?fedora} > 25
# For early testing of rhbz#1400293 mozbz#1324096 on F26 and Rawhide,
# temporarily require the specific NSS build with the backports.
# Can be removed after firefox is changed to require NSS 3.30.
BuildRequires:  nss-devel >= 3.29.1-2.1
Requires:       nss >= 3.29.1-2.1
%endif

%if 0%{?fedora} < 26
# Using Conflicts for p11-kit, not Requires, because on multi-arch
# systems p11-kit isn't yet available for secondary arches like
# p11-kit.i686 (fallback to libnssckbi.so from NSS).
# This build contains backports from p11-kit 0.23.4
Conflicts: p11-kit < 0.23.2-3
# Requires build with CKA_NSS_MOZILLA_CA_POLICY attribute
Requires: ca-certificates >= 2017.2.11-1.1
# Requires NSS build with backports from NSS 3.30
BuildRequires:  nss-devel >= 3.29.3-1.1
Requires:       nss >= 3.29.3-1.1
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  system-bookmarks
%if %{?system_sqlite}
BuildRequires:  pkgconfig(sqlite3) >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif

%if %{?system_ffi}
BuildRequires:  pkgconfig(libffi)
%endif

%if %{?run_tests}
BuildRequires:  xorg-x11-server-Xvfb
%endif
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  clang-devel

Obsoletes:      mozilla <= 37:1.7.13
Provides:       webclient

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%if %{enable_mozilla_crashreporter}
%global moz_debug_prefix %{_prefix}/lib/debug
%global moz_debug_dir %{moz_debug_prefix}%{mozappdir}
%global uname_m %(uname -m)
%global symbols_file_name %{name}-%{version}.en-US.%{_os}-%{uname_m}.crashreporter-symbols.zip
%global symbols_file_path %{moz_debug_dir}/%{symbols_file_name}
%global _find_debuginfo_opts -p %{symbols_file_path} -o debugcrashreporter.list
%global crashreporter_pkg_name mozilla-crashreporter-%{name}-debuginfo
%package -n %{crashreporter_pkg_name}
Summary: Debugging symbols used by Mozilla's crash reporter servers
%description -n %{crashreporter_pkg_name}
This package provides debug information for Firefox, for use by
Mozilla's crash reporter servers.  If you are trying to locally
debug %{name}, you want to install %{name}-debuginfo instead.
%files -n %{crashreporter_pkg_name} -f debugcrashreporter.list
%endif

%if %{?wayland_backend_default}
%package x11
Summary: Firefox X11 launcher.
Requires: %{name}
%description x11
The firefox-x11 package contains launcher and desktop file
to run Firefox natively on X11.
%files x11
%{_bindir}/firefox-x11
%{_datadir}/applications/firefox-x11.desktop
%else
%package wayland
Summary: Firefox Wayland launcher.
Requires: %{name}
%description wayland
The firefox-wayland package contains launcher and desktop file
to run Firefox natively on Wayland.
%files wayland
%{_bindir}/firefox-wayland
%{_datadir}/applications/firefox-wayland.desktop
%endif


%if %{run_tests}
%global testsuite_pkg_name mozilla-%{name}-testresults
%package -n %{testsuite_pkg_name}
Summary: Results of testsuite
%description -n %{testsuite_pkg_name}
This package contains results of tests executed during build.
%files -n %{testsuite_pkg_name}
/test_results
%endif

#---------------------------------------------------------------------

%prep
%setup -q -n %{tarballdir}

# Build patches, can't change backup suffix from default because during build
# there is a compare of config and js/config directories and .orig suffix is
# ignored during this compare.


%ifarch s390
%patch25 -p1 -b .rhbz-1219542-s390
%endif
%patch37 -p1 -b .jit-atomic-lucky
%patch40 -p1 -b .aarch64-skia
%if 0%{?disable_elfhack}
%patch41 -p1 -b .disable-elfhack
%endif
%patch3  -p1 -b .arm
%patch42 -p1 -b .nss-build
%patch43 -p1 -b .1500366
%patch44 -p1 -b .1494037

# Fedora patches
%patch215 -p1 -b .addons
%patch219 -p2 -b .rhbz-1173156
%patch221 -p2 -b .fedora-ua
%patch224 -p1 -b .1170092
#ARM run-time patch
%ifarch aarch64
%patch226 -p1 -b .1354671
%endif

%patch402 -p1 -b .1196777
%patch406 -p1 -b .256180
%patch413 -p1 -b .1353817
%ifarch %{arm}
%patch415 -p1 -b .1238661
%endif
# Patch for big endian platforms only
%if 0%{?big_endian}
%patch26 -p1 -b .icu
%endif
%patch421 -p1 -b .1447775

# Wayland specific upstream patches
%patch573 -p1 -b .1415078
%if 0%{?fedora} > 27
%patch574 -p1 -b .firefox-pipewire
%endif
%patch581 -p1 -b .mozilla-1493081

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig
echo "ac_add_options --enable-default-toolkit=cairo-gtk3-wayland" >> .mozconfig
%if %{official_branding}
echo "ac_add_options --enable-official-branding" >> .mozconfig
%endif
%{__cp} %{SOURCE24} mozilla-api-key
%{__cp} %{SOURCE27} google-api-key

%if %{?system_nss}
echo "ac_add_options --with-system-nspr" >> .mozconfig
echo "ac_add_options --with-system-nss" >> .mozconfig
%else
echo "ac_add_options --without-system-nspr" >> .mozconfig
echo "ac_add_options --without-system-nss" >> .mozconfig
%endif

%if %{?system_sqlite}
echo "ac_add_options --enable-system-sqlite" >> .mozconfig
%else
echo "ac_add_options --disable-system-sqlite" >> .mozconfig
%endif

%if %{?system_cairo}
echo "ac_add_options --enable-system-cairo" >> .mozconfig
%else
echo "ac_add_options --disable-system-cairo" >> .mozconfig
%endif

%if %{?system_ffi}
echo "ac_add_options --enable-system-ffi" >> .mozconfig
%endif

%ifarch %{arm}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
%else
%global optimize_flags "none"
%ifarch armv7hl
# ARMv7 needs that (rhbz#1426850)
%global optimize_flags "-g -O2 -fno-schedule-insns"
# Disable libaom due to rhbz#1641623
echo "ac_add_options --disable-av1" >> .mozconfig
%endif
%ifarch ppc64le aarch64
%global optimize_flags "-g -O2"
%endif
%if %{optimize_flags} != "none"
echo 'ac_add_options --enable-optimize=%{?optimize_flags}' >> .mozconfig
%else
echo 'ac_add_options --enable-optimize' >> .mozconfig
%endif
echo "ac_add_options --disable-debug" >> .mozconfig
%endif

# Second arches fail to start with jemalloc enabled
%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif

%if !%{enable_mozilla_crashreporter}
echo "ac_add_options --disable-crashreporter" >> .mozconfig
%endif

%if %{?run_tests}
echo "ac_add_options --enable-tests" >> .mozconfig
%endif

%if !%{?system_jpeg}
echo "ac_add_options --without-system-jpeg" >> .mozconfig
%else
echo "ac_add_options --with-system-jpeg" >> .mozconfig
%endif

%if %{?system_libvpx}
echo "ac_add_options --with-system-libvpx" >> .mozconfig
%else
echo "ac_add_options --without-system-libvpx" >> .mozconfig
%endif

%if %{?system_libicu}
echo "ac_add_options --with-system-icu" >> .mozconfig
%else
echo "ac_add_options --without-system-icu" >> .mozconfig
%endif
%ifarch s390 s390x
echo "ac_add_options --disable-ion" >> .mozconfig
%endif

# Remove executable bit to make brp-mangle-shebangs happy.
chmod -x third_party/rust/itertools/src/lib.rs

%if 0%{?use_bundled_cbindgen}

mkdir -p my_rust_vendor
cd my_rust_vendor
%{__tar} xf %{SOURCE2}
cd -
mkdir -p .cargo
cat > .cargo/config <<EOL
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "`pwd`/my_rust_vendor"
EOL

env CARGO_HOME=.cargo cargo install cbindgen
%endif
#---------------------------------------------------------------------

%build
%if %{?system_sqlite}
# Do not proceed with build if the sqlite require would be broken:
# make sure the minimum requirement is non-empty, ...
sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
# ... and that major number of the computed build-time version matches:
case "%{sqlite_build_version}" in
  "$sqlite_version"*) ;;
  *) exit 1 ;;
esac
%endif

%if 0%{?use_bundled_cbindgen}
export PATH=`pwd`/.cargo/bin:$PATH
%endif

echo "Generate big endian version of config/external/icu/data/icud58l.dat"
%if 0%{?big_endian}
  ./mach python intl/icu_sources_data.py .
  ls -l config/external/icu/data
  rm -f config/external/icu/data/icudt*l.dat
%endif

# Update the various config.guess to upstream release for aarch64 support
find ./ -name config.guess -exec cp /usr/lib/rpm/config.guess {} ';'

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
#
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "%{optflags}" | %{__sed} -e 's/-Wall//')
#rhbz#1037063
# -Werror=format-security causes build failures when -Wno-format is explicitly given
# for some sources
# Explicitly force the hardening flags for Firefox so it passes the checksec test;
# See also https://fedoraproject.org/wiki/Changes/Harden_All_Packages
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
%if 0%{?fedora} > 23
# Disable null pointer gcc6 optimization in gcc6 (rhbz#1328045)
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fno-delete-null-pointer-checks"
%endif
# Use hardened build?
%if %{?hardened_build}
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fPIC -Wl,-z,relro -Wl,-z,now"
%endif
%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
# If MOZ_DEBUG_FLAGS is empty, firefox's build will default it to "-g" which
# overrides the -g1 from line above and breaks building on s390
# (OOM when linking, rhbz#1238225)
export MOZ_DEBUG_FLAGS=" "
%endif
%ifarch s390 %{arm} ppc aarch64 %{ix86}
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
%ifarch %{arm}
export RUSTFLAGS="-Cdebuginfo=0"
%endif
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le aarch64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

#make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"
export MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"
export MOZ_SERVICES_SYNC="1"
export STRIP=/bin/true
./mach build

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
#cd %{moz_objdir}
make -C objdir buildsymbols
%endif

%if %{?run_tests}
%if %{?system_nss}
ln -s /usr/bin/certutil objdir/dist/bin/certutil
ln -s /usr/bin/pk12util objdir/dist/bin/pk12util

%endif
mkdir test_results
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey || true
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey-2nd-run || true
./mach --log-no-times cppunittest &> test_results/cppunittest || true
xvfb-run ./mach --log-no-times crashtest &> test_results/crashtest || true
./mach --log-no-times gtest &> test_results/gtest || true
xvfb-run ./mach --log-no-times jetpack-test &> test_results/jetpack-test || true
# not working right now ./mach marionette-test &> test_results/marionette-test || true
xvfb-run ./mach --log-no-times mochitest-a11y &> test_results/mochitest-a11y || true
xvfb-run ./mach --log-no-times mochitest-browser &> test_results/mochitest-browser || true
xvfb-run ./mach --log-no-times mochitest-chrome &> test_results/mochitest-chrome || true
xvfb-run ./mach --log-no-times mochitest-devtools &> test_results/mochitest-devtools || true
xvfb-run ./mach --log-no-times mochitest-plain &> test_results/mochitest-plain || true
xvfb-run ./mach --log-no-times reftest &> test_results/reftest || true
xvfb-run ./mach --log-no-times webapprt-test-chrome &> test_results/webapprt-test-chrome || true
xvfb-run ./mach --log-no-times webapprt-test-content &> test_results/webapprt-test-content || true
./mach --log-no-times webidl-parser-test &> test_results/webidl-parser-test || true
xvfb-run ./mach --log-no-times xpcshell-test &> test_results/xpcshell-test || true
%if %{?system_nss}
rm -f  objdir/dist/bin/certutil
rm -f  objdir/dist/bin/pk12util
%endif

%endif
#---------------------------------------------------------------------

%install

# set up our default bookmarks
%{__cp} -p %{default_bookmarks_file} objdir/dist/bin/browser/chrome/en-US/locale/browser/bookmarks.html

# Make sure locale works for langpacks
%{__cat} > objdir/dist/bin/browser/defaults/preferences/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF

DESTDIR=%{buildroot} make -C objdir install

%{__mkdir_p} %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE20}
%if %{?wayland_backend_default}
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE31}
%else
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE29}
%endif

# set up the firefox start script
%if %{?wayland_backend_default}
%global x11_state false
%else
%global x11_state true
%endif
%{__rm} -rf %{buildroot}%{_bindir}/firefox
%{__sed} -e 's/__DEFAULT_X11__/%{x11_state}/' %{SOURCE21} > %{buildroot}%{_bindir}/firefox

%{__chmod} 755 %{buildroot}%{_bindir}/firefox
%if %{?wayland_backend_default}
%{__cat} %{SOURCE30} > %{buildroot}%{_bindir}/firefox-x11
%{__chmod} 755 %{buildroot}%{_bindir}/firefox-x11
%else
%{__cat} %{SOURCE28} > %{buildroot}%{_bindir}/firefox-wayland
%{__chmod} 755 %{buildroot}%{_bindir}/firefox-wayland
%endif

%{__install} -p -D -m 644 %{SOURCE23} %{buildroot}%{_mandir}/man1/firefox.1

%{__rm} -f %{buildroot}/%{mozappdir}/firefox-config
%{__rm} -f %{buildroot}/%{mozappdir}/update-settings.ini

for s in 16 22 24 32 48 256; do
    %{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
    %{__cp} -p browser/branding/official/default${s}.png \
               %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/firefox.png
done

# Install hight contrast icon
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps
%{__cp} -p %{SOURCE25} \
           %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p %{buildroot}%{_datadir}/appdata
cat > %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: https://bugzilla.mozilla.org/show_bug.cgi?id=1071061
SentUpstream: 2014-09-22
-->
<application>
  <id type="desktop">firefox.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Bringing together all kinds of awesomeness to make browsing better for you.
      Get to your favorite sites quickly – even if you don’t remember the URLs.
      Type your term into the location bar (aka the Awesome Bar) and the autocomplete
      function will include possible matches from your browsing history, bookmarked
      sites and open tabs.
    </p>
    <!-- FIXME: Needs another couple of paragraphs -->
  </description>
  <url type="homepage">http://www.mozilla.org/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/a.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/b.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/c.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

echo > %{name}.lang
%if %{with langpacks}
# Extract langpacks, make any mods needed, repack the langpack, and install it.
%{__mkdir_p} %{buildroot}%{langpackdir}
%{__tar} xf %{SOURCE1}
for langpack in `ls firefox-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensionID=langpack-$language@firefox.mozilla.org
  %{__mkdir_p} $extensionID
  unzip -qq $langpack -d $extensionID
  find $extensionID -type f | xargs chmod 644

  cd $extensionID
  zip -qq -r9mX ../${extensionID}.xpi *
  cd -

  %{__install} -m 644 ${extensionID}.xpi %{buildroot}%{langpackdir}
  language=`echo $language | sed -e 's/-/_/g'`
  echo "%%lang($language) %{langpackdir}/${extensionID}.xpi" >> %{name}.lang
done
%{__rm} -rf firefox-langpacks

# Install langpack workaround (see #707100, #821169)
function create_default_langpack() {
language_long=$1
language_short=$2
cd %{buildroot}%{langpackdir}
ln -s langpack-$language_long@firefox.mozilla.org.xpi langpack-$language_short@firefox.mozilla.org.xpi
cd -
echo "%%lang($language_short) %{langpackdir}/langpack-$language_short@firefox.mozilla.org.xpi" >> %{name}.lang
}

# Table of fallbacks for each language
# please file a bug at bugzilla.redhat.com if the assignment is incorrect
create_default_langpack "bn-IN" "bn"
create_default_langpack "es-AR" "es"
create_default_langpack "fy-NL" "fy"
create_default_langpack "ga-IE" "ga"
create_default_langpack "gu-IN" "gu"
create_default_langpack "hi-IN" "hi"
create_default_langpack "hy-AM" "hy"
create_default_langpack "nb-NO" "nb"
create_default_langpack "nn-NO" "nn"
create_default_langpack "pa-IN" "pa"
create_default_langpack "pt-PT" "pt"
create_default_langpack "sv-SE" "sv"
create_default_langpack "zh-TW" "zh"
%endif # with langpacks


%{__mkdir_p} %{buildroot}/%{mozappdir}/browser/defaults/preferences

# System config dir
%{__mkdir_p} %{buildroot}/%{_sysconfdir}/%{name}/pref

# System extensions
%{__mkdir_p} %{buildroot}%{_datadir}/mozilla/extensions/%{firefox_app_id}
%{__mkdir_p} %{buildroot}%{_libdir}/mozilla/extensions/%{firefox_app_id}

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE %{buildroot}/%{mozappdir}

# Use the system hunspell dictionaries
%{__rm} -rf %{buildroot}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell %{buildroot}%{mozappdir}/dictionaries

# Enable crash reporter for Firefox application
%if %{enable_mozilla_crashreporter}
sed -i -e "s/\[Crash Reporter\]/[Crash Reporter]\nEnabled=1/" %{buildroot}/%{mozappdir}/application.ini
# Add debuginfo for crash-stats.mozilla.com
%{__mkdir_p} %{buildroot}/%{moz_debug_dir}
%{__cp} objdir/dist/%{symbols_file_name} %{buildroot}/%{moz_debug_dir}
%endif

%if %{run_tests}
# Add debuginfo for crash-stats.mozilla.com
%{__mkdir_p} %{buildroot}/test_results
%{__cp} test_results/* %{buildroot}/test_results
%endif

# Default
%{__cp} %{SOURCE12} %{buildroot}%{mozappdir}/browser/defaults/preferences

# Copy over run-mozilla.sh
%{__cp} build/unix/run-mozilla.sh %{buildroot}%{mozappdir}

# Add distribution.ini
%{__mkdir_p} %{buildroot}%{mozappdir}/distribution
%{__cp} %{SOURCE26} %{buildroot}%{mozappdir}/distribution

# Remove copied libraries to speed up build
rm -f %{buildroot}%{mozappdirdev}/sdk/lib/libmozjs.so
rm -f %{buildroot}%{mozappdirdev}/sdk/lib/libmozalloc.so
rm -f %{buildroot}%{mozappdirdev}/sdk/lib/libxul.so
#---------------------------------------------------------------------

# Moves defaults/preferences to browser/defaults/preferences
%pretrans -p <lua>
require 'posix'
require 'os'
if (posix.stat("%{mozappdir}/browser/defaults/preferences", "type") == "link") then
  posix.unlink("%{mozappdir}/browser/defaults/preferences")
  posix.mkdir("%{mozappdir}/browser/defaults/preferences")
  if (posix.stat("%{mozappdir}/defaults/preferences", "type") == "directory") then
    for i,filename in pairs(posix.dir("%{mozappdir}/defaults/preferences")) do
      os.rename("%{mozappdir}/defaults/preferences/"..filename, "%{mozappdir}/browser/defaults/preferences/"..filename)
    end
    f = io.open("%{mozappdir}/defaults/preferences/README","w")
    if f then
      f:write("Content of this directory has been moved to %{mozappdir}/browser/defaults/preferences.")
      f:close()
    end
  end
end


%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
  %{__rm} -rf %{mozappdir}/extensions
  %{__rm} -rf %{mozappdir}/plugins
  %{__rm} -rf %{langpackdir}
fi

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%{_bindir}/firefox
%{mozappdir}/firefox
%{mozappdir}/firefox-bin
%doc %{_mandir}/man1/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/*
%dir %{_datadir}/mozilla/extensions/*
%dir %{_libdir}/mozilla/extensions/*
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/%{name}.desktop
%dir %{mozappdir}
%license %{mozappdir}/LICENSE
%{mozappdir}/browser/chrome
%{mozappdir}/browser/chrome.manifest
%{mozappdir}/browser/defaults/preferences/firefox-redhat-default-prefs.js
%{mozappdir}/browser/features/*.xpi
%{mozappdir}/distribution/distribution.ini
# That's Windows only
%ghost %{mozappdir}/browser/features/aushelper@mozilla.org.xpi
%attr(644, root, root) %{mozappdir}/browser/blocklist.xml
#%dir %{mozappdir}/browser/extensions
#%{mozappdir}/browser/extensions/*
%if %{with langpacks}
%dir %{langpackdir}
%endif
%{mozappdir}/browser/omni.ja
%{mozappdir}/chrome.manifest
%{mozappdir}/run-mozilla.sh
%{mozappdir}/application.ini
%{mozappdir}/pingsender
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/firefox.png
%{_datadir}/icons/hicolor/22x22/apps/firefox.png
%{_datadir}/icons/hicolor/24x24/apps/firefox.png
%{_datadir}/icons/hicolor/256x256/apps/firefox.png
%{_datadir}/icons/hicolor/32x32/apps/firefox.png
%{_datadir}/icons/hicolor/48x48/apps/firefox.png
%{_datadir}/icons/hicolor/symbolic/apps/firefox-symbolic.svg
%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/minidump-analyzer
%{mozappdir}/Throbber-small.gif
%{mozappdir}/browser/crashreporter-override.ini
%endif
%{mozappdir}/*.so
%{mozappdir}/gtk2/*.so
%{mozappdir}/defaults/pref/channel-prefs.js
%{mozappdir}/dependentlibs.list
%{mozappdir}/dictionaries
%{mozappdir}/omni.ja
%{mozappdir}/platform.ini
%{mozappdir}/plugin-container
%{mozappdir}/gmp-clearkey
%{mozappdir}/fonts/TwemojiMozilla.ttf
%if !%{?system_nss}
%{mozappdir}/libfreeblpriv3.chk
%{mozappdir}/libnssdbm3.chk
%{mozappdir}/libsoftokn3.chk
%exclude %{mozappdir}/libnssckbi.so
%endif

#---------------------------------------------------------------------

%changelog
* Thu Nov 1 2018 Martin Stransky <stransky@redhat.com> - 63.0.1-2
- Fixed typo on man page (rhbz#1643766)

* Thu Nov 1 2018 Martin Stransky <stransky@redhat.com> - 63.0.1-1
- Updated to latest upstream (63.0.1 build 4)

* Tue Oct 23 2018 Martin Stransky <stransky@redhat.com> - 63.0-2
- Updated to latest upstream (63.0 build 2)

* Thu Oct 18 2018 Martin Stransky <stransky@redhat.com> - 63.0-1
- Updated to latest upstream (63.0)
- Updated PipeWire patch

* Tue Oct 9 2018 Martin Stransky <stransky@redhat.com> - 62.0.3-4
- Added fix for mozbz#1447775 - wrong dropspace sizing.

* Tue Oct 9 2018 Martin Stransky <stransky@redhat.com> - 62.0.3-3
- Added fix for mozbz#1493081 - popups incorrectly placed and sized.

* Mon Oct 8 2018 Martin Stransky <stransky@redhat.com> - 62.0.3-2
- Added pipewire patch (mozbz#1496359)
- Added Wayland patches from Firefox 63
- Enable Wayland backed by default on Fedora 30

* Tue Oct 2 2018 Martin Stransky <stransky@redhat.com> - 62.0.3-1
- Updated to latest upstream (62.0.3)

* Wed Sep 26 2018 Martin Stransky <stransky@redhat.com> - 62.0.2-3
- Enabled DBus remote for all Gtk+ backends
- Removed obsoleted patches

* Tue Sep 25 2018 Martin Stransky <stransky@redhat.com> - 62.0.2-2
- Disable workaround for mozbz#1342344 - GFX glitches when building
  with -O3/gcc 7.2

* Mon Sep 24 2018 Jan Horak <jhorak@redhat.com> - 62.0.2-1
- Update to 62.0.2

* Mon Sep 17 2018 Martin Stransky <stransky@redhat.com> - 62.0-3
- Added spellchecker.dictionary_path pref pointer to /usr/share/myspell.
  Thanks to Peter Oliver (rhbz#1627837)

* Tue Sep 4 2018 Martin Stransky <stransky@redhat.com> - 62.0-2
- Update to 62.0 (Build 2)

* Tue Aug 28 2018 Martin Stransky <stransky@redhat.com> - 62.0-1
- Update to 62.0

* Wed Aug 15 2018 Ondrej Zoder <ozoder@redhat.com> - 61.0.2-3
- Added patches for mozbz#1427700 and mozbz#1463809

* Mon Aug 13 2018 Ondrej Zoder <ozoder@redhat.com> - 61.0.2-2
- Updated symbolic icon

* Thu Aug 9 2018 Martin Stransky <stransky@redhat.com> - 61.0.2-1
- Update to 61.0.2

* Wed Aug 1 2018 Ondrej Zoder <ozoder@redhat.com> - 61.0.1-4
- Fixed rhbz#1610428

* Tue Jul 17 2018 Ondrej Zoder <ozoder@redhat.com> - 61.0.1-3
- Bump release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 61.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Ondrej Zoder <ozoder@redhat.com> - 61.0.1
- Update to 61.0.1

* Mon Jun 25 2018 Martin Stransky <stransky@redhat.com> - 61.0-4
- Disabled mozbz#1424422 as it's broken.

* Fri Jun 22 2018 Martin Stransky <stransky@redhat.com> - 61.0-3
- Update to 61.0 Build 3

* Thu Jun 21 2018 Martin Stransky <stransky@redhat.com> - 61.0-2
- Disabled system hunspell due to rhbz#1593494

* Tue Jun 19 2018 Martin Stransky <stransky@redhat.com> - 61.0-1
- Updated to 61.0
- Created firefox-wayland subpackage with wayland launcher.

* Mon Jun 11 2018 Jan Horak <jhorak@redhat.com> - 60.0.2-1
- Update to 60.0.2

* Mon Jun 4 2018 Martin Stransky <stransky@redhat.com> - 60.0.1-6
- Fixed mozbz#1466473, rhbz#1585300 - Fix GL detection.
- Fixed desktop file names (rhbz#1585369).

* Wed May 30 2018 Martin Stransky <stransky@redhat.com> - 60.0.1-5
- Added workaround for mozbz#1464823 which makes GL layer
  compositor usable on Wayland.

* Tue May 29 2018 Martin Stransky <stransky@redhat.com> - 60.0.1-4
- Added fix for mozbz#1464808 - Set default D&D action to move
  on Wayland.

* Fri May 25 2018 Martin Stransky <stransky@redhat.com> - 60.0.1-3
- Added fix for mozbz#1436242 (rhbz#1577277) - Firefox IPC crashes.
- Added fix for mozbz#1462640 - Sandbox disables eglGetDisplay()
  call on Wayland/EGL backend.

* Fri May 25 2018 Martin Stransky <stransky@redhat.com> - 60.0.1-2
- Enable Wayland backend.

* Wed May 23 2018 Jan Horak <jhorak@redhat.com> - 60.0.1-1
- Update to 60.0.1

* Wed May 16 2018 Martin Stransky <stransky@redhat.com> - 60.0-6
- Added patch from rhbz#1498561 - second arch (ppc*) crashes.

* Wed May 16 2018 Martin Stransky <stransky@redhat.com> - 60.0-5
- Disabled jemalloc on second arches.

* Thu May 3 2018 Martin Stransky <stransky@redhat.com> - 60.0-4
- Updated to Firefox 60 build 2

* Thu May 3 2018 Martin Stransky <stransky@redhat.com> - 60.0-3
- Added patch from mozbz#1375074 - fixes aarch64 baseline JIT crashes

* Thu May 3 2018 Martin Stransky <stransky@redhat.com> - 60.0-2
- Make Wayland backend optional and disable it by default due to WebGL issues.

* Wed May 2 2018 Martin Stransky <stransky@redhat.com> - 60.0-1
- Update to Firefox 60 build 1
- Ship firefox-wayland launch script

* Mon Apr 30 2018 Martin Stransky <stransky@redhat.com> - 60.0-0.5
- Build with Wayland backend enabled.

* Mon Apr 30 2018 Martin Stransky <stransky@redhat.com> - 60.0-0.4
- Added patches for correct popups position at CSD mode (mozilla-1457691).

* Fri Apr 27 2018 Martin Stransky <stransky@redhat.com> - 60.0-0.2
- Update to 60.0 Beta 16

* Tue Apr 24 2018 Martin Stransky <stransky@redhat.com> - 60.0-0.1
- Update to 60.0 Beta 15

