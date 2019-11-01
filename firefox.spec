# Set to true if it's going to be submitted as update.
%global release_build     1

# Disabled arm due to rhbz#1658940
ExcludeArch: armv7hl
# Disabled due to https://pagure.io/fedora-infrastructure/issue/7581
ExcludeArch: s390x
# Disabled due to build error rhbz#1749729
%if 0%{?fedora} < 30
ExcludeArch: ppc64le
%endif

%global system_nss        1
%global system_ffi        1
# libvpx is too new for Firefox 65
%if 0%{?fedora} < 30
%global system_libvpx     1
%else
%global system_libvpx     0
%endif
%global hardened_build    1
%global system_jpeg       1
%global run_tests         0
%global disable_elfhack   1
%global build_with_clang  0
%global use_bundled_cbindgen  1
# Build PGO+LTO on x86_64 and aarch64 only due to build issues
# on other arches.
%ifarch x86_64 aarch64
%if %{release_build}
%global build_with_pgo    1
%else
%global build_with_pgo    0
%endif
# Build PGO builds on Wayland backend
%global pgo_wayland       0
%endif
%if 0%{?fedora} > 30
%global wayland_backend_default 1
%endif
%if 0%{?flatpak}
%global wayland_backend_default 1
%global build_with_pgo    0
%endif
# Big endian platforms
%ifarch ppc64 s390x
%global big_endian        1
%endif
%global debug_build       0

%if 0%{?build_with_pgo}
%global use_xvfb          1
%global build_tests       1
%endif

%if !0%{?run_tests}
%global use_xvfb          1
%global build_tests       1
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
%global nspr_version 4.21
%global nspr_build_version %{nspr_version}
%global nss_version 3.45
%global nss_build_version %{nss_version}
%endif

%global mozappdir     %{_libdir}/%{name}
%global mozappdirdev  %{_libdir}/%{name}-devel-%{version}
%global langpackdir   %{mozappdir}/langpacks
%global tarballdir    firefox-%{version}

%global official_branding       1

%bcond_without langpacks

# Disable crashreporter as we want to collect Wayland crashes.
%global enable_mozilla_crashreporter       0

%if !%{release_build}
%global pre_tag .test
%endif

Summary:        Mozilla Firefox Web browser
Name:           firefox
Version:        70.0.1
Release:        1%{?pre_tag}%{?dist}
URL:            https://www.mozilla.org/firefox/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Source0:        https://archive.mozilla.org/pub/firefox/releases/%{version}%{?pre_version}/source/firefox-%{version}%{?pre_version}.source.tar.xz
%if %{with langpacks}
Source1:        firefox-langpacks-%{version}%{?pre_version}-20191101.tar.xz
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
Source32:       node-stdout-nonblocking-wrapper

# Build patches
Patch3:         mozilla-build-arm.patch
Patch25:        rhbz-1219542-s390-build.patch
Patch26:        build-icu-big-endian.patch
Patch32:        build-rust-ppc64le.patch
Patch35:        build-ppc-jit.patch
# Always feel lucky for unsupported platforms:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1347128
Patch37:        build-jit-atomic-always-lucky.patch
# Fixing missing cacheFlush when JS_CODEGEN_NONE is used (s390x)
Patch38:        build-cacheFlush-missing.patch
Patch40:        build-aarch64-skia.patch
Patch41:        build-disable-elfhack.patch
Patch44:        build-arm-libopus.patch
#Patch45:        build-disable-multijobs-rust.patch
Patch46:        firefox-nss-version.patch

# Fedora specific patches
Patch215:        firefox-enable-addons.patch
Patch219:        rhbz-1173156.patch
Patch221:        firefox-fedora-ua.patch
Patch224:        mozilla-1170092.patch
#ARM run-time patch
Patch226:        rhbz-1354671.patch
Patch227:        firefox-locale-debug.patch
Patch228:        mozilla-1583466.patch

# Upstream patches
Patch402:        mozilla-1196777.patch
Patch412:        mozilla-1337988.patch
Patch415:        Bug-1238661---fix-mozillaSignalTrampoline-to-work-.patch
Patch417:        bug1375074-save-restore-x28.patch
Patch419:        mozilla-1568569.patch
Patch421:        mozilla-1579023.patch
Patch422:        mozilla-1580174-webrtc-popup.patch

# Wayland specific upstream patches
Patch574:        firefox-pipewire.patch
Patch575:        mozilla-1548475.patch
Patch590:        firefox-wayland-cache-missing.patch
Patch591:        mozilla-1587008.patch

# PGO/LTO patches
Patch600:        pgo.patch
Patch601:        mozilla-1516081.patch
Patch602:        mozilla-1516803.patch

%if %{?system_nss}
BuildRequires:  pkgconfig(nspr) >= %{nspr_version}
BuildRequires:  pkgconfig(nss) >= %{nss_version}
BuildRequires:  nss-static >= %{nss_version}
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
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  yasm
BuildRequires:  llvm
BuildRequires:  llvm-devel
BuildRequires:  clang
BuildRequires:  clang-libs
%if 0%{?build_with_clang}
BuildRequires:  lld
%endif
BuildRequires:  pipewire-devel
%if !0%{?use_bundled_cbindgen}
BuildRequires:  cbindgen
%endif
BuildRequires:  nodejs
BuildRequires:  nasm >= 1.13

Requires:       mozilla-filesystem
Requires:       p11-kit-trust
%if %{?system_nss}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif
BuildRequires:  python2-devel
%if !0%{?flatpak}
Requires:       u2f-hidraw-policy
%endif

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
%if !0%{?flatpak}
BuildRequires:  system-bookmarks
%endif
%if %{?system_ffi}
BuildRequires:  pkgconfig(libffi)
%endif

%if 0%{?use_xvfb}
BuildRequires:  xorg-x11-server-Xvfb
%endif
%if 0%{?pgo_wayland}
BuildRequires:  mutter
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

%if 0%{?wayland_backend_default}
%package x11
Summary: Firefox X11 launcher.
Requires: %{name}
%description x11
The firefox-x11 package contains launcher and desktop file
to run Firefox explicitly on X11.
%files x11
%{_bindir}/firefox-x11
%{_datadir}/applications/firefox-x11.desktop
%endif

%package wayland
Summary: Firefox Wayland launcher.
Requires: %{name}
%description wayland
The firefox-wayland package contains launcher and desktop file
to run Firefox explicitly on Wayland.
%files wayland
%{_bindir}/firefox-wayland
%{_datadir}/applications/firefox-wayland.desktop

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
#%patch37 -p1 -b .jit-atomic-lucky
%patch40 -p1 -b .aarch64-skia
%if 0%{?disable_elfhack}
%patch41 -p1 -b .disable-elfhack
%endif
%patch3  -p1 -b .arm
%patch44 -p1 -b .build-arm-libopus
#%patch45 -p1 -b .build-disable-multijobs-rust
# Patch for big endian platforms only
%if 0%{?big_endian}
%patch26 -p1 -b .icu
%endif
%patch46 -p1 -b .nss-version

# Fedora patches
%patch215 -p1 -b .addons
%patch219 -p1 -b .rhbz-1173156
%patch221 -p1 -b .fedora-ua
%patch224 -p1 -b .1170092
#ARM run-time patch
%ifarch aarch64
%patch226 -p1 -b .1354671
%endif
%patch227 -p1 -b .locale-debug
%patch228 -p1 -b .mozilla-1583466

%patch402 -p1 -b .1196777
%ifarch %{arm}
%patch415 -p1 -b .1238661
%endif
%patch419 -p1 -b .1568569
%patch421 -p1 -b .1579023

# Wayland specific upstream patches
%patch574 -p1 -b .firefox-pipewire
%patch575 -p1 -b .mozilla-1548475
%patch590 -p1 -b .cache-missing
%patch591 -p1 -b .mozilla-1587008

# PGO patches
%patch600 -p1 -b .pgo
%patch601 -p1 -b .1516081
%patch602 -p1 -b .1516803

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

%ifnarch %{ix86} x86_64 ppc64le
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif

%if !%{enable_mozilla_crashreporter}
echo "ac_add_options --disable-crashreporter" >> .mozconfig
%endif

%if 0%{?build_tests}
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

%ifarch s390 s390x
echo "ac_add_options --disable-ion" >> .mozconfig
%endif

echo 'export NODEJS="%{_buildrootdir}/bin/node-stdout-nonblocking-wrapper"' >> .mozconfig

# Remove executable bit to make brp-mangle-shebangs happy.
chmod -x third_party/rust/itertools/src/lib.rs

#---------------------------------------------------------------------

%build
%if 0%{?use_bundled_cbindgen}

mkdir -p my_rust_vendor
cd my_rust_vendor
%{__tar} xf %{SOURCE2}
mkdir -p .cargo
cat > .cargo/config <<EOL
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "`pwd`"
EOL

env CARGO_HOME=.cargo cargo install cbindgen
export PATH=`pwd`/.cargo/bin:$PATH
%endif
cd -

echo "Generate big endian version of config/external/icu/data/icud58l.dat"
%if 0%{?big_endian}
  ./mach python intl/icu_sources_data.py .
  ls -l config/external/icu/data
  rm -f config/external/icu/data/icudt*l.dat
%endif

mkdir %{_buildrootdir}/bin || :
cp %{SOURCE32} %{_buildrootdir}/bin || :

# Update the various config.guess to upstream release for aarch64 support
find ./ -name config.guess -exec cp /usr/lib/rpm/config.guess {} ';'

MOZ_OPT_FLAGS=$(echo "%{optflags}" | %{__sed} -e 's/-Wall//')
#rhbz#1037063
# -Werror=format-security causes build failures when -Wno-format is explicitly given
# for some sources
# Explicitly force the hardening flags for Firefox so it passes the checksec test;
# See also https://fedoraproject.org/wiki/Changes/Harden_All_Packages
%if 0%{?fedora} < 30
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
%else
# Workaround for mozbz#1531309
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-Werror=format-security//')
%endif
%if 0%{?fedora} > 30
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fpermissive"
%endif
%if %{?hardened_build}
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fPIC -Wl,-z,relro -Wl,-z,now"
%endif
%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
# If MOZ_DEBUG_FLAGS is empty, firefox's build will default it to "-g" which
# overrides the -g1 from line above and breaks building on s390/arm
# (OOM when linking, rhbz#1238225)
export MOZ_DEBUG_FLAGS=" "
%endif
%ifarch %{arm} %{ix86}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g0/')
export MOZ_DEBUG_FLAGS=" "
%endif
%if !0%{?build_with_clang}
%ifarch s390 ppc aarch64 %{ix86}
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
%ifarch %{arm}
MOZ_LINK_FLAGS="-Wl,--no-keep-memory"
echo "ac_add_options --enable-linker=gold" >> .mozconfig
%endif
%endif
%if 0%{?flatpak}
# Make sure the linker can find libraries in /app/lib64 as we don't use
# __global_ldflags that normally sets this.
MOZ_LINK_FLAGS="$MOZ_LINK_FLAGS -L%{_libdir}"
%endif
%ifarch %{arm} %{ix86}
export RUSTFLAGS="-Cdebuginfo=0"
%endif
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

%if 0%{?build_with_clang}
export LLVM_PROFDATA="llvm-profdata"
export AR="llvm-ar"
export NM="llvm-nm"
export RANLIB="llvm-ranlib"
echo "ac_add_options --enable-linker=lld" >> .mozconfig
%else
export CC=gcc
export CXX=g++
export AR="gcc-ar"
export NM="gcc-nm"
export RANLIB="gcc-ranlib"
%endif
%if 0%{?build_with_pgo}
echo "ac_add_options MOZ_PGO=1" >> .mozconfig
echo "ac_add_options --enable-lto" >> .mozconfig
%endif

MOZ_SMP_FLAGS=-j1
# On x86_64 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86}
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
%endif
%ifarch x86_64 ppc ppc64 ppc64le aarch64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

export MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"
export MOZ_SERVICES_SYNC="1"
export STRIP=/bin/true
%if 0%{?build_with_pgo}
%if 0%{?pgo_wayland}
xvfb-run mutter --wayland --nested &
if [ -z "$WAYLAND_DISPLAY" ]; then
  export WAYLAND_DISPLAY=wayland-0
else
  export WAYLAND_DISPLAY=wayland-1
fi
MOZ_ENABLE_WAYLAND=1 ./mach build  2>&1 | cat -
%else
GDK_BACKEND=x11 xvfb-run ./mach build  2>&1 | cat -
%endif
%else
./mach build -v 2>&1 | cat -
%endif

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
make -C objdir buildsymbols
%endif

%if %{?run_tests}
%if %{?system_nss}
ln -s %{_prefix}/bin/certutil objdir/dist/bin/certutil
ln -s %{_prefix}/bin/pk12util objdir/dist/bin/pk12util

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
%if !0%{?flatpak}
%{__cp} -p %{default_bookmarks_file} objdir/dist/bin/browser/chrome/en-US/locale/browser/bookmarks.html
%endif

# Make sure locale works for langpacks
%{__cat} > objdir/dist/bin/browser/defaults/preferences/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF

DESTDIR=%{buildroot} make -C objdir install

%{__mkdir_p} %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE20}
%if 0%{?wayland_backend_default}
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE31}
%endif
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE29}

# set up the firefox start script
%if 0%{?wayland_backend_default}
%global wayland_default true
%else
%global wayland_default false
%endif
%{__rm} -rf %{buildroot}%{_bindir}/firefox
%{__sed} -e 's/__DEFAULT_WAYLAND__/%{wayland_default}/' \
         -e 's,/__PREFIX__,%{_prefix},g' %{SOURCE21} > %{buildroot}%{_bindir}/firefox
%{__chmod} 755 %{buildroot}%{_bindir}/firefox


%if 0%{?flatpak}
sed -i -e 's|%FLATPAK_ENV_VARS%|export TMPDIR="$XDG_CACHE_HOME/tmp"|' %{buildroot}%{_bindir}/firefox
%else
sed -i -e 's|%FLATPAK_ENV_VARS%||' %{buildroot}%{_bindir}/firefox
%endif

%if 0%{?wayland_backend_default}
%{__sed} -e 's,/__PREFIX__,%{_prefix},g' %{SOURCE30} > %{buildroot}%{_bindir}/firefox-x11
%{__chmod} 755 %{buildroot}%{_bindir}/firefox-x11
%endif
%{__sed} -e 's,/__PREFIX__,%{_prefix},g' %{SOURCE28} > %{buildroot}%{_bindir}/firefox-wayland
%{__chmod} 755 %{buildroot}%{_bindir}/firefox-wayland

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
%if 0%{?flatpak}
  echo "%{langpackdir}/${extensionID}.xpi" >> %{name}.lang
%else
  echo "%%lang($language) %{langpackdir}/${extensionID}.xpi" >> %{name}.lang
%endif
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
#create_default_langpack "bn-IN" "bn"
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
* Fri Nov 1 2019 Martin Stransky <stransky@redhat.com> - 70.0.1-1
- Updated to 70.0.1
- Built with system-nss (reverted 70.0-2 change).

* Thu Oct 31 2019 Martin Stransky <stransky@redhat.com> - 70.0-2
- Switched to in-tree nss due to rhbz#1752303

* Tue Oct 15 2019 Martin Stransky <stransky@redhat.com> - 70.0-1
- Updated to 70.0

* Mon Oct 14 2019 Martin Stransky <stransky@redhat.com> - 69.0.3-2
- Build firefox-wayland again (rhbz#1761578).

* Thu Oct 10 2019 Martin Stransky <stransky@redhat.com> - 69.0.3-1
- Updated to 69.0.3

* Wed Oct 9 2019 Martin Stransky <stransky@redhat.com> - 69.0.2-3
- Obsolete firefox-wayland when we're on wayland by default.

* Thu Oct 3 2019 Martin Stransky <stransky@redhat.com> - 69.0.2-2
- Added fix for mozilla#1587008 - flickering during GL resize.

* Thu Oct 3 2019 Martin Stransky <stransky@redhat.com> - 69.0.2-1
- Updated to 69.0.2

* Mon Sep 30 2019 Martin Stransky <stransky@redhat.com> - 69.0.1-5
- Updated rhbz#1754460/mzbz#1583466 - per user policy dir.

* Tue Sep 24 2019 Martin Stransky <stransky@redhat.com> - 69.0.1-4
- Added fix for rhbz#1754460

* Thu Sep 19 2019 Martin Stransky <stransky@redhat.com> - 69.0.1-3
- Updated cache-missing strategy for Wayland image cache.

* Thu Sep 19 2019 Martin Stransky <stransky@redhat.com> - 69.0.1-2
- Do PGO builds with X11 backend.

* Wed Sep 18 2019 Martin Stransky <stransky@redhat.com> - 69.0.1-1
- Updated to 69.0.1

* Wed Sep 18 2019 Martin Stransky <stransky@redhat.com> - 69.0-11
- Do PGO builds with Wayland backend.

* Wed Sep 18 2019 Martin Stransky <stransky@redhat.com> - 69.0-10
- Disabled DoH by default (rhbz#1751410),
  patch by Eduardo Mínguez Pérez (eminguez).

* Tue Sep 17 2019 Martin Stransky <stransky@redhat.com> - 69.0-9
- Enable Wayland cache mode control (mozbz#1577024)

* Tue Sep 17 2019 Martin Stransky <stransky@redhat.com> - 69.0-7
- Added fixes for mozbz#1581748

* Mon Sep 16 2019 Martin Stransky <stransky@redhat.com> - 69.0-6
- Added fixes for mozbz#1579823, mozbz#1580152

* Wed Sep 11 2019 Martin Stransky <stransky@redhat.com> - 69.0-5
- Added fix for mozbz#1579849 - partial screen update when
  page switches.

* Wed Sep 11 2019 Martin Stransky <stransky@redhat.com> - 69.0-4
- Added fix for mozbz#1579794 - Flickering on video playback on
  4k/HiDPI displays.

* Mon Sep 9 2019 Martin Stransky <stransky@redhat.com> - 69.0-3
- Added fix for mozbz#1579023

* Mon Sep 2 2019 Martin Stransky <stransky@redhat.com> - 69.0-2
- Added upstream Wayland patches (mozilla-1548475, mozilla-1562827,
  mozilla-1567434, mozilla-1573813, mozilla-1574036,
  mozilla-1576268).
- Enable multiprocess compilation.
- Enable profile downgrade.
- Disabled ppc64le on Fedora 29 (rhbz#1749729)

* Thu Aug 29 2019 Jan Horak <jhorak@redhat.com> - 69.0-1
- Update to 69.0

* Wed Aug 14 2019 Jan Horak <jhorak@redhat.com> - 68.0.2-1
- Update to 68.0.2

* Mon Aug  5 2019 Jan Horak <jhorak@redhat.com> - 68.0.1-3
- Added workaround fix for webrtc indicator
- Added rust build workaround

* Wed Jul 24 2019 Martin Stransky <stransky@redhat.com> - 68.0.1-2
- Added fix for rhbz#1709840
- Added node js wrapper to fix koji freezes
  (https://pagure.io/fedora-infrastructure/issue/8026)
- Updated mozbz#1512162 for ppc64le

* Mon Jul 22 2019 Martin Stransky <stransky@redhat.com> - 68.0.1-1
- Updated to 68.0.1
- Enabled WebRTC on ppc64le (rhbz#1732069)

* Thu Jul 11 2019 Martin Stransky <stransky@redhat.com> - 68.0-5
- Enabled aarch64 and ppc64le

* Wed Jul 10 2019 Martin Stransky <stransky@redhat.com> - 68.0-4
- Added fixes for aarch64 builds.

* Tue Jul  9 2019 Dan Horák <dan[at]danny.cz> - 68.0-3
- Fix crash on ppc64le (mozilla#1512162)

* Mon Jul  8 2019 Jan Horak <jhorak@redhat.com> - 68.0-2
- Update pipewire patch

* Tue Jul 2 2019 Martin Stransky <stransky@redhat.com> - 68.0-1
- Updated to 68.0

* Thu Jun 20 2019 Martin Stransky <stransky@redhat.com> - 67.0.4-1
- Updated to 67.0.4

* Tue Jun 18 2019 Martin Stransky <stransky@redhat.com> - 67.0.3-1
- Updated to 67.0.3

* Tue Jun 11 2019 Martin Stransky <stransky@redhat.com> - 67.0.2-1
- Updated to 67.0.2 Build 2

* Thu May 23 2019 Martin Stransky <stransky@redhat.com> - 67.0-4
- Added wayland buffer optimization (mozilla#1553747).

* Fri May 17 2019 Martin Stransky <stransky@redhat.com> - 67.0-3
- Use %lang() in regular builds.
- Updated to 67.0 Build 2

* Thu May 16 2019 Jan Horak <jhorak@redhat.com> - 67.0-2
- Removed %lang() prefix from langpacks file list due to flatpak

* Wed May 15 2019 Martin Stransky <stransky@redhat.com> - 67.0-1
- Updated to 67.0

* Wed May 8 2019 Martin Stransky <stransky@redhat.com> - 66.0.5-1
- Updated to 66.0.5

* Sun May 5 2019 Martin Stransky <stransky@redhat.com> - 66.0.4-1
- Updated to 66.0.4

* Thu May 2 2019 Martin Stransky <stransky@redhat.com> - 66.0.3-2
- Removed fix for mozbz#526293 as it's broken and does not
  bring any new functionality.

* Thu Apr 11 2019 Martin Stransky <stransky@redhat.com> - 66.0.3-1
- Updated to 66.0.3 (Build 1)

* Mon Apr 1 2019 Martin Stransky <stransky@redhat.com> - 66.0.2-1
- Updated to 66.0.2 (Build 1)
- Added fixes for mozbz#1526243, mozbz#1540145

* Thu Mar 28 2019 Martin Stransky <stransky@redhat.com> - 66.0.1-4
- Added fix for mozbz#1539471 - wayland popups/tooltips

* Wed Mar 27 2019 Martin Stransky <stransky@redhat.com> - 66.0.1-3
- Added fix for mozbz#526293 - show remote locations at
  file chooser dialog

* Fri Mar 22 2019 Martin Stransky <stransky@redhat.com> - 66.0.1-1
- Updated to 66.0.1 (Build 1)

* Thu Mar 21 2019 Martin Stransky <stransky@redhat.com> - 66.0-10.test
- Test module build, use flatpak global define
- Added fix for F31 (mozbz#1533969)

* Thu Mar 21 2019 Martin Stransky <stransky@redhat.com> - 66.0-9
- Release build

* Thu Mar 21 2019 Martin Stransky <stransky@redhat.com> - 66.0-8.test
- Added module specific build config
- Fixed mozbz#1423598 for multi-monitor setup

* Wed Mar 20 2019 Martin Stransky <stransky@redhat.com> - 66.0-7.test
- Switched to test builds
- Updated mozbz#1468911 patch

* Mon Mar 18 2019 Martin Stransky <stransky@redhat.com> - 66.0-6
- Build release candidate
- Disabled default Wayland backend for Fedora 30

* Mon Mar 18 2019 Martin Stransky <stransky@redhat.com> - 66.0-5
- Added fix for mozbz#1468911

* Mon Mar 18 2019 Martin Stransky <stransky@redhat.com> - 66.0-4
- Release build

* Fri Mar 15 2019 Martin Stransky <stransky@redhat.com> - 66.0-3
- Updated to 66.0 (Build 3)
- Re-enable s390x arches
- Fixed Wayland specific bugs mozbz#1535567, mozbz#1431399

* Tue Mar 12 2019 Martin Stransky <stransky@redhat.com> - 66.0-1
- Updated to 66.0 (Build 1)

* Fri Mar 1 2019 Martin Stransky <stransky@redhat.com> - 65.0.2-1
- Updated to 65.0.2
- Disabled PGO+LTO for Fedora 30
- Disabled Mozilla Crashreporter to get Wayland crashes by ABRT
- Disabled s390x builds due to
  https://pagure.io/fedora-infrastructure/issue/7581


* Thu Feb 28 2019 Martin Stransky <stransky@redhat.com> - 65.0.1-2
- Enable ARBT for Fedora 29 and later to catch wayland crashes.
- Disable system libvpx for Fedora 30 and later.

* Wed Feb 20 2019 Martin Stransky <stransky@redhat.com> - 65.0.1-1
- Disabled s390x/f28 builds due to
  https://pagure.io/fedora-infrastructure/issue/7581

* Fri Feb 15 2019 Jan Horak <jhorak@redhat.com> - 65.0.1-1
- Update to 65.0.1

* Mon Feb 4 2019 Martin Stransky <stransky@redhat.com> - 65.0-4
- Added fix for mozbz#1522780

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 65.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 31 2019 Jan Grulich <jgrulich@redhat.com> - 65.0-2
- Re-enable PipeWire support

* Mon Jan 28 2019 Martin Stransky <stransky@redhat.com> - 65.0-1
- Update to 65.0 build 2

* Wed Jan 16 2019 Martin Stransky <stransky@redhat.com> - 64.0.2-2
- Rebuild

* Thu Jan 10 2019 Jan Horak <jhorak@redhat.com> - 64.0.2-1
- Update to 64.0.2

* Mon Jan  7 2019 Jan Horak <jhorak@redhat.com> - 64.0-7
- Pipewire patch rebased (thanks to Tomas Popela)
- Enabled PGO on some arches.

* Fri Jan 4 2019 Carmen Bianca Bakker <carmenbianca@fedoraproject.org> - 64.0-6
- Changed locale detector to handle Esperanto (rhbz#1656900)

* Fri Dec 21 2018 Martin Stransky <stransky@redhat.com> - 64.0-5
- Test PGO build.

* Wed Dec 12 2018 Martin Stransky <stransky@redhat.com> - 64.0-4
- Use gcc on all platforms for official release.

* Wed Dec 12 2018 Martin Stransky <stransky@redhat.com> - 64.0-3
- Updated PGO build setup.

* Tue Dec 4 2018 Martin Stransky <stransky@redhat.com> - 64.0-2
- Updated to Firefox 64 (Build 3)
- Built with Clang on some arches.

* Mon Nov 26 2018 Martin Stransky <stransky@redhat.com> - 63.0.3-3
- [Wayland] Fixed issues with Sway compositor and wl_keyboard setup
  (mozbz#1507475).

* Wed Nov 21 2018 Martin Stransky <stransky@redhat.com> - 63.0.3-2
- [Wayland] Fixed mozbz#1507475 - crash when display changes
  (rhbz#1646151).

* Thu Nov 15 2018 Martin Stransky <stransky@redhat.com> - 63.0.3-1
- Updated to latest upstream (63.0.3)

* Tue Nov 13 2018 Martin Stransky <stransky@redhat.com> - 63.0.1-6
- Added an option to build with clang/llvm.
- Fixed debug builds.
- Fixed warnings at Wayland clipboard code.

* Tue Nov 6 2018 Martin Stransky <stransky@redhat.com> - 63.0.1-5
- Added fix for mozbz#1502457- disable Contextual Feature
  Recommender/shield studies by default.

* Mon Nov 5 2018 Martin Stransky <stransky@redhat.com> - 63.0.1-4
- Added clipboard fix (mozbz#1504689)

* Fri Nov 2 2018 Dan Horak <dhorak@redhat.com> - 63.0.1-3
- Added fixes for ppc64le

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
