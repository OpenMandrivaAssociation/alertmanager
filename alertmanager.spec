Name:		alertmanager
Version:	0.21.0
Release:        3
Summary:	The Alertmanager handles alerts sent by client applications such as the Prometheus server.
Group:		System Environment/Daemons
License:	See the LICENSE file at github.
URL:		https://github.com/prometheus/alertmanager
Source0:	https://github.com/prometheus/alertmanager/archive/v%{version}.tar.gz
Source1:	alertmanager.service
Source2:	alertmanager.sysconfig
BuildRequires:	promu
BuildRequires:	golang
Requires:	prometheus
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
AutoReqProv:    No

%description
The Alertmanager handles alerts sent by client applications such as the Prometheus server.
It takes care of deduplicating, grouping, and routing them to the correct receiver integration such as email, PagerDuty, or OpsGenie. 
It also takes care of silencing and inhibition of alerts.

%prep
%autosetup -p1
mkdir -p src/github.com/prometheus/
ln -s ../../../ src/github.com/prometheus/alertmanager

%build
export GOPATH=$(pwd):%{gopath}
promu build

%install
mkdir -vp %{buildroot}/var/log/prometheus/
mkdir -vp %{buildroot}/var/run/prometheus
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/%{_bindir}
mkdir -vp %{buildroot}/etc/prometheus/alertmanager
mkdir -vp %{buildroot}/%{_unitdir}
mkdir -vp %{buildroot}/%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/alertmanager.service
install -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/alertmanager
install -m 644 doc/examples/simple.yml %{buildroot}/etc/prometheus/alertmanager/alertmanager.yaml
install -m 755 alertmanager %{buildroot}/usr/bin/alertmanager
install -m 755 amtool %{buildroot}/usr/bin/amtool

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -s /sbin/nologin \
    -d %{buildroot}/var/lib/prometheus/ -c "prometheus Daemons" prometheus
exit 0

%post
chgrp prometheus /var/run/prometheus
chmod 774 /var/run/prometheus
chown prometheus:prometheus /var/log/prometheus
chmod 744 /var/log/prometheus

%files
%{_bindir}/alertmanager
%{_bindir}/amtool
%config(noreplace) %{_sysconfdir}/prometheus/alertmanager/alertmanager.yaml
%config(noreplace) %{_sysconfdir}/sysconfig/alertmanager
%{_unitdir}/alertmanager.service
