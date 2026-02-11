# vim: syntax=spec

%global srcname acpi_call
%global debug_package %{nil}

Name:       acpi_call-dkms
Version:    1.2.2
Release:    1%{?dist}
Summary:    A linux kernel module that enables calls to ACPI methods through /proc/acpi/call.
License:    GPLv3
URL:        https://github.com/RheaAyase/acpi_call.rpm
Source:     https://github.com/RheaAyase/acpi_call.rpm/releases/latest/download/acpi_call-dkms-1.2.2.tar.gz

Provides: acpi_call

Requires: dkms
Requires: kernel-devel
Requires: make
Requires: gcc

%description
A linux kernel module that enables calls to ACPI methods through /proc/acpi/call.

%prep
%setup -C

%install
install -D -m 0644 %{srcname}/*.c -t "%{buildroot}%{_usrsrc}/%{srcname}-%{version}/"
install -m 0644 Makefile "%{buildroot}%{_usrsrc}/%{srcname}-%{version}/"
install -m 0644 dkms.conf "%{buildroot}%{_usrsrc}/%{srcname}-%{version}/"

%post
dkms add -m acpi_call -v %{version} --rpm_safe_upgrade
dkms build -m acpi_call -v %{version} --rpm_safe_upgrade
dkms install -m acpi_call -v %{version} --rpm_safe_upgrade
modprobe %{srcname} && echo "%{srcname}" > %{_sysconfdir}/modules-load.d/%{srcname}.conf

%preun
rmmod ${srcname} || : 
rm %{_sysconfdir}/modules-load.d/%{srcname}.conf || :
dkms remove -m ${srcname} -v %{version} --all --rpm_safe_upgrade || :

%postun
rm -rfv %{_usrsrc}/%{srcname}-%{version}

%files
%{_usrsrc}/%{srcname}-%{version}/%{srcname}.c
%{_usrsrc}/%{srcname}-%{version}/Makefile
%{_usrsrc}/%{srcname}-%{version}/dkms.conf

%changelog
* Mon Feb 12 2026 Rhea Gustavsson <contact@rhea.dev> 1.2.2-1
- init

