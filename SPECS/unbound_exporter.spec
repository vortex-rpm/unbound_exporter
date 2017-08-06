%define debug_package %{nil}

%define _git_url https://github.com/kumina/unbound_exporter
%define _git_slug src/github.com/kumina/unbound_exporter

Name:    unbound_exporter
Version: 0.0
Release: 0.f538243git.vortex%{?dist}
Summary: Prometheus exporter for unbound
License: MIT
Vendor:  Vortex RPM
URL:     https://github.com/kumina/unbound_exporter

Source1: %{name}.service
Source2: %{name}.default

Requires(pre): shadow-utils
%{?el7:%{?systemd_requires}}
BuildRequires: golang, git

%description
Prometheus exporter for unbound.

%prep
mkdir _build
export GOPATH=$(pwd)/_build
git clone %{_git_url} $GOPATH/%{_git_slug}
cd $GOPATH/%{_git_slug}
# git checkout v%{version}

%build
export GOPATH=$(pwd)/_build
cd $GOPATH/%{_git_slug}
go get -v .
got build -v unbound_exporter.go
strip %{name}

%install
export GOPATH=$(pwd)/_build
mkdir -vp %{buildroot}/var/lib/prometheus
%{?el7:mkdir -vp %{buildroot}/usr/bin}
%{?el7:mkdir -vp %{buildroot}/usr/lib/systemd/system}
mkdir -vp %{buildroot}/etc/default
%{?el7:install -m 755 $GOPATH/%{_git_slug}/%{name} %{buildroot}/usr/bin/%{name}}
%{?el7:install -m 755 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service}
install -m 644 %{SOURCE2} %{buildroot}/etc/default/%{name}

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%{?el7:%systemd_post %{name}.service}

%preun
%{?el7:%systemd_preun %{name}.service}

%postun
%{?el7:%systemd_postun %{name}.service}

%files
%defattr(-,root,root,-)
%{?el7:/usr/bin/%{name}}
%{?el7:/usr/lib/systemd/system/%{name}.service}
%config(noreplace) /etc/default/%{name}
%attr(755, prometheus, prometheus)/var/lib/prometheus
%doc _build/%{_git_slug}/LICENSE _build/%{_git_slug}/README.md

%changelog
* Sun Aug 06 2017 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 0.0-0.f538243git.vortex
- Initial packaging
