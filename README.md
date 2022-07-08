# نحوه اجرای پروژه 

ابتدا نرم‌افزارهای [vagrant](https://www.vagrantup.com/downloads) و [virtualbox](https://www.virtualbox.org/wiki/Downloads) را دانلود و نصب کنید. سپس با دستور زیر پروژه‌ی sigcomm20_mptp_tutorial را clone کنید.

    git clone https://github.com/qdeconinck/sigcomm20_mptp_tutorial.git

حال در ترمینال به پوشه sigcomm20_mptp_tutorial رفته و در آنجا دستور زیر را اجرا می کنیم.

    vagrant up

اگر این دستور کار نکرد می توانیم فایل اجرایی vagrant را در همان پوشه sigcomm20_mptp_tutorial قرار دهیم.

اگر سیستم عامل ویندوز را دارید قبل از دستور قبل باید دستور زیر را وارد کنید.

    chcp 1252

در حالت ایده آل دستور vagrant up باید ابتدا سیستم عامل مجازی لینوکس با کرنل مجهز به MPTCP را ایجاد کرده و سپس Mininet، Minitopo، openflow و ... را ایجاد کرده و آماده به کار شود. اما در تجربه شخصی خود مشاهده کردیم که به ایراداتی بر می خورد لذا زمانی که مانند شکل زیر سیستم عامل مجازی در virtualBox ایجاد شد و دستور vagrant up تمام شد دیگر با vagrant کار نمی کنیم و از virtualBox سیستم عامل مجازی خود را کنترل می کنیم


<p align="center">
<img src="https://github.com/hamidreza7799/mptcp/blob/master/InstallationGuide1.jpg?raw=true">
</p>

برای آنکه اتصال به اینترنت ماشین مجازی فعال شود باید ماشین مجازی خود را خاموش کرده و به قسمت تنظیمات آن رفته و در بخش network، آداپتور NAT را به Bridged Adaptor تغییر دهید.

<p align="center">
<img src="https://github.com/hamidreza7799/mptcp/blob/master/InstallationGuide2.jpg?raw=true">
</p>

سپس سیستم عامل مجازی خود را روشن می کنیم. نام کاربری و گذرواژه vagrant می باشد. سپس باید دستور زیر را بنویسیم.

    curl https://www.multipath-tcp.org

اگر جواب yes را دریافت کردیم به این معنی است که ارتباط به صورت mptcp برقرار شده است و مشکلی در کرنل لینوکس مجهز به mptcp وجود نداشته است.اما اگر به جواب no برخوردیم باید یا پروسه را از اول شروع کرده یا از روش های دیگر کرنل لینوکس مجهز به mptcp را نصب کنیم. این روش ها در سایت [multipath-tcp.org](https://multipath-tcp.org) آمده است.

می توانیم دستورات زیر را درون سیستم عامل مجازی اجرا کرده و کرنل لینوکس مجهز به mptcp را نصب کنیم.


    wget https://github.com/multipath-tcp/mptcp/releases/download/v0.94.7/linux-headers-4.14.146.mptcp_20190924124242_amd64.deb

    wget https://github.com/multipath-tcp/mptcp/releases/download/v0.94.7/linux-image-4.14.146.mptcp_20190924124242_amd64.deb

    wget https://github.com/multipath-tcp/mptcp/releases/download/v0.94.7/linux-libc-dev_20190924124242_amd64.deb

    wget https://github.com/multipath-tcp/mptcp/releases/download/v0.94.7/linux-mptcp-4.14_v0.94.7_20190924124242_all.deb

    sudo dpkg -i linux-*.deb

    # The following runs the MPTCP kernel version 4.14.146 as the default one

    sudo cat /etc/default/grub | sed -e "s/GRUB_DEFAULT=0/GRUB_DEFAULT='Advanced options for Ubuntu>Ubuntu, with Linux 4.14.146.mptcp'/" > tmp_grub

    sudo mv tmp_grub /etc/default/grub

    sudo update-grub

    # Finally ask for MPTCP module loading at the loadtime

    echo "
    # Load MPTCP modules
    sudo modprobe mptcp_olia
    sudo modprobe mptcp_coupled
    sudo modprobe mptcp_balia
    sudo modprobe mptcp_wvegas

    # Schedulers
    sudo modprobe mptcp_rr
    sudo modprobe mptcp_redundant
    # The following line will likely not work with versions of MPTCP < 0.95
    sudo modprobe mptcp_blest

    # Path managers
    sudo modprobe mptcp_ndiffports
    sudo modprobe mptcp_binder" | sudo tee -a /etc/bash.bashrc
    
حال باید mininet و minitopo را نصب کنیم. برای اینکار ابتدا source code ها را از git گرفته و هر کدام را نصب می کنیم.

    git clone https://github.com/mininet/mininet

سپس دستورات زیر را وارد می کنیم.

    cd mininet

    git tag  # list available versions

    git checkout -b mininet-2.3.0 2.3.0  # or whatever version you wish to install

سپس دستور زیر را وارد می کنیم تا mininet نصب شود.

    util/install.sh -a

تعداد پکیج هایی که دستور فوق نصب می کند زیاد است لذا مدت زمان قابل توجهی طول می کشد تا نصب شود.
اگر هنگام نصب به مشکلی خوردید چندبار دیگر هم دستور بالا را اجرا کنید. اگر هنگام clone کردن openflow به مشکل برخوردیم باید در فایل util/install.sh تغییراتی را ایجاد کنیم. در این فایل باید همه //:git ها را به //:https تغییر دهیم (5 مورد). برای مثال مانند زیر خط اول را به خط دوم تبدیل می کنیم.

    git clone git://github.com/mininet/openflow
    git clone https://github.com/mininet/openflow

سپس دستور util/install.sh را اجرا می کنیم.

حال دستور زیر را می نویسیم تا مطمئن شویم که mininet درست نصب شده است.

    sudo mn

سپس exit را می نوسیم تا از محیط CLI مینینت خارج شویم.

حال به مسیر home/vagrant رفته و دستور زیر را اجرا می کنیم تا کد minitopo را دریافت کنیم.

    git clone https://github.com/qdeconinck/minitopo.git

سپس دستور زیر را می نویسیم تا کد های این پروژه را نیز داشته باشیم.

    git clone https://github.com/hamidreza7799/mptcp.git

برای تعیین حالت های مختلف الگوریتم های کنترل ازدحام و مدیریت مسیر و کنترل ازدحام در minitop لازم است که در فایل minitopo/experiments/iperf_scenario.py از چهار دستور زیر استفاده کنیم که در حالت های مختلف بعضی از آن ها کامنت و بعضی از آن ها از کامنت خارج می شوند.

```python
self.topo.command_global("modprobe mptcp_rr && sysctl -w net.mptcp.mptcp_scheduler=roundrobin")

self.topo.command_global("modprobe mptcp_ndiffports && sysctl -w net.mptcp.mptcp_path_manager=ndiffports ")

self.topo.command_global("echo 2 | sudo tee /sys/module/mptcp_ndiffports/parameters/num_subflows ")
```

برای مثال می خواهیم حالت LIA، Fullmesh، LR را اجرا کنیم. به پوشه lia_fullmesh_rtt می رویم و دستور های زیر را اجرا می کنیم.

    python3 configuration.py -m 1

    python3 configuration.py


دستور اول این خطوط را اضافه کرده و دستور دوم با توجه به پوشه ای که در آن اجرا می شود خطوط را کامنت می کند یا از کامنت خارج می سازد. (برای پوشه های بعدی فقط دستور دوم استفاده می شود)

حال دستور زیر را وارد می کنیم تا به اجرای minitopo ایرادی نگیرد.

    git config --global -add safe.directory /home/vagrant/minitopo

برای اینکه بتوانیم هر یک از حالت ها را 50 بار آزمایش کنیم باید در هر پوشه دستور زیر را اجرا کنیم.

    ./run.sh

این دستور باعث می شود که iperf کلاینت mptcp در هر بار اجرا ذخیره گردد. در run.sh از minitopo برای شبیه سازی استفاده می شود که فایلی را به عنوان توپولوژی و فایل دیگری را به عنوان experiment دریافت می کند. فایل experiment نیز به iperf_scenario.py اشاره می کند و برای تغییر در توپولوژی و سناریو باید این فایل را تغییر بدهیم.