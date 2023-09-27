FROM kalilinux/kali-rolling

ARG gid
ARG uid
ARG group
ARG user

# Update packages and upgrade system

RUN apt-get update && apt-get -y upgrade && apt-get -y dist-upgrade && apt-get -y autoremove && apt-get -y clean && apt-get install -y sudo git fish tmux

RUN groupadd -g ${gid} ${group} && useradd -m -u ${uid} -g ${gid} -G ${group} -s /usr/bin/fish ${user}
RUN chown -R ${user}:${group} /home/${user}
RUN echo "${user}    ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN apt install -y kali-tools-top10 feroxbuster nmap metasploit-framework python3-impacket hashcat john hydra proxychains sshuttle xsser wpscan evil-winrm whatweb nikto apktool dex2jar dirb man-db steghide theharvester lsof

USER ${user}

# Install Tmux
RUN git clone https://github.com/gpakosz/.tmux.git "/home/${user}/.oh-my-tmux"
RUN mkdir -p "/home/${user}/.config/tmux"
RUN ln -s "/home/${user}/.oh-my-tmux/.tmux.conf" "/home/${user}/.config/tmux/tmux.conf"
COPY --chown=${user}:${group} ./dotfiles/.tmux.conf.local "/home/${user}/.config/tmux/tmux.conf.local"

ENTRYPOINT ["tail", "-f", "/dev/null"]