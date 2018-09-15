# Hstctl
`Hstctl` lets you easily manage and structure your `/etc/hosts` file.

# Installation
Clone the repository:\
`$ git clone https://github.com/JannikHv/hstctl`

Switch to the repo's directory:\
`$ cd hstctl`

Install hstctl:\
`$ sudo python setup.py install`


# Usage
| Option               | Parameter    | Description                                                                 |
|:---------------------|:-------------|:----------------------------------------------------------------------------|
| `-h` / `--help`      | `/`          | Print help.                                                                 |\
| `-i` / `--ips`       | `IPS`        | IPs specifier.                                                              |\
| `-a` / `--add`       | `HOSTNAMES`  | Add hostnames to entries by IPs (`-i`).                                     |\
| `-r` / `--remove`    | `HOSTNAMES`  | Remove hostnames from entries by IPs (`-i`).                                |\
| `-e` / `--enable`    | `IPS`        | Enable entries by given IPs.                                                |\
| `-d` / `--disable`   | `IPS`        | Disable entries by given IPs.                                               |\
| `-p` / `--purge`     | `IPS`        | Purge entries by given IPs.                                                 |\
| `-c` / `--comment`   | `COMMENT`    | Comment entries by IPs (`-i`).                                              |\
| `-u` / `--uncomment` | `IPS`        | Uncomment entries by given IPs.                                             |\
| `-s` / `--show`      | `IPS`        | Show entries of given IPs.                                                  |\
| `-l` / `--list`      | `/`          | List all entries.                                                           |\
| `-o` / `--optimize`  | `/`          | Optimize your `/etc/hosts` file (auto: `-a`/`-r`/`-e`/`-d`/`-p`/`-c`/`-u`). |

| Parameter   | Description                         | Example                       |
|:------------|:------------------------------------|:------------------------------|
| `IPS`       | IP Addresses (separated by spaces). | `"192.168.12.24 192.168.1.1"` |
| `HOSTNAMES` | Hostnames (separated by spaces).    | `"github.com google.com"`     |
| `COMMENT`   | Comment/Note.                       | `"Dev server"`                |

#### Annotations
An `entry` describes one **IP** paired with one or more **hostnames**.\
The optimization `-o` automatically applies when changes have been made (`-a`/`-r`/`-e`/`-d`/`-p`/`-c`/`-u`).

# Examples
**Add** hostnames to entries by IPs:\
`$ sudo hstctl -i "192.168.12.24 192.168.1.1" -a "github.com google.com"`

**Remove** hostname from entry by IP:\
`$ sudo hstctl -i 192.168.12.24 -r google.com`

**Enable** entries by IPs:\
`$ sudo hstctl -e "192.168.12.24 192.168.1.1"`

**Disable** entry by IP:\
`$ sudo hstctl -d 192.168.12.24`

**Purge** entries by IPs:\
`$ sudo hstctl -p "192.168.12.24 192.168.1.1"`

**Comment** entry by IP:\
`$ sudo hstctl -i 192.168.12.24 -c "Dev server"`

**Uncomment** entries by IPs:\
`$ sudo hstctl -u "192.168.12.24 192.168.1.1"`

**Show** entries by IPs:\
`$ hstctl -s "192.168.12.24 192.168.1.1"`

**List** all entries:\
`$ hstctl -l`

**Optimize** your /etc/hosts file:\
`$ sudo hstctl -o`

Combining options with `-l` will always list you the end-result.

# TODO
- [ ] Add an option for verbose output.
- [ ] Create an installer.
- [ ] Create an AUR package.

# Author
Jannik "JannikHv" Hauptvogel

**·
[Twitter](https://twitter.com/JannikHv) ·
[GitHub](https://github.com/JannikHv) ·
[GitLab](https://gitlab.com/JannikHv)
·**
