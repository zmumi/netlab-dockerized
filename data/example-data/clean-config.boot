system {
    login {
        user vyos {
            authentication {
                encrypted-password "$1$5HsQse2v$VQLh5eeEp4ZzGmCG/PRBA1"
            }
            level admin
        }
    }
    package {
        repository community {
	    distribution "helium"
            components "main"
            url "http://packages.vyos.net/vyos"
        }
    }
    syslog {
        global {
            facility all {
                level notice
            }
            facility protocols {
                level debug
            }
        }
    }
    ntp {
        server "0.pool.ntp.org"
        server "1.pool.ntp.org"
        server "2.pool.ntp.org"
    }
    console {
        device ttyS0 {
            speed 9600
        }
    }
    config-management {
        commit-revisions 20
    }
}

interfaces {
ethernet eth0 {
        address dhcp
    }
    loopback lo {
    }
}


/* Warning: Do not remove the following line. */
/* === vyatta-config-version: "qos@1:cron@1:vrrp@1:dhcp-server@4:system@6:ipsec@4:wanloadbalance@3:webgui@1:nat@4:cluster@1:webproxy@1:conntrack@1:firewall@5:zone-policy@1:quagga@2:config-management@1:conntrack-sync@1:dhcp-relay@1" === */
/* Release version: VyOS 1.1.1 */
