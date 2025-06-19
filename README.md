# Matrix Version 2 Project / پروژه Matrix نسخه ۲

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)  
A project to set up a Matrix Version 2 server using Docker, Traefik, and Synapse. This is a work-in-progress, primarily for demonstration and idea-sharing purposes.  
پروژه‌ای برای راه‌اندازی سرور Matrix نسخه ۲ با استفاده از داکر، Traefik و Synapse. این پروژه هنوز در حال توسعه است و بیشتر برای نمایش و به اشتراک‌گذاری ایده‌ها طراحی شده است.


---

### Overview / مرور کلی
This project aims to provide a Matrix Version 2 server setup using Docker, Traefik for routing, and Synapse as the Matrix homeserver. It includes services like Element Web, Sliding Sync, and Matrix Authentication Service. The project is under active development and serves as a proof-of-concept.  
این پروژه با هدف ارائه راه‌اندازی سرور Matrix نسخه ۲ با استفاده از داکر، Traefik برای مسیریابی، و Synapse به عنوان سرور خانگی Matrix طراحی شده است. این شامل سرویس‌هایی مانند Element Web، Sliding Sync و سرویس احراز هویت Matrix است. پروژه در حال توسعه فعال است و به عنوان یک مفهوم آزمایشی عمل می‌کند.

---

### Prerequisites / پیش‌نیازها
Before starting, ensure you have the following:  
قبل از شروع، مطمئن شوید که موارد زیر را دارید:
- A server running a Linux distribution (e.g., Debian 12) / سروری با توزیع لینوکس (مانند Debian 12)
- Docker and Docker Compose installed / داکر و داکر کامپوز نصب شده
- A domain name with DNS configured / نام دامنه با DNS پیکربندی شده
- Python and `uv` for generating configuration files / پایتون و `uv` برای تولید فایل‌های پیکربندی

---

### Setup Instructions / دستورالعمل راه‌اندازی

#### 1. Generate Configuration Files / تولید فایل‌های پیکربندی
Run the following command locally to generate configuration files:  
دستور زیر را به صورت محلی اجرا کنید تا فایل‌های پیکربندی تولید شوند:
```bash
uv run python src/create_config.py
```
This will create a `dist/config` folder containing the necessary configuration files.  
این دستور یک پوشه `dist/config` حاوی فایل‌های پیکربندی مورد نیاز ایجاد می‌کند.

#### 2. Configure Environment Variables / پیکربندی متغیرهای محیطی
Copy the `env.example.yml` file to `env.yml` and fill in the appropriate values for each field:  
فایل `env.example.yml` را به `env.yml` کپی کنید و مقادیر مناسب را برای هر فیلد وارد کنید:
```bash
cp env.example.yml env.yml
```
Edit `.env` to set values for variables like `V_MAIN_DOMAIN`, `V_SERVER_ADDRESS`, `V_PASS`, etc.  
فایل `.env` را ویرایش کنید تا مقادیر متغیرهایی مانند `V_MAIN_DOMAIN`، `V_SERVER_ADDRESS`، `V_PASS` و غیره را تنظیم کنید.

#### 3. Transfer Configurations to Server / انتقال پیکربندی‌ها به سرور
Copy the `dist/config` folder and `.env` file to your server. For example, using `scp`:  
پوشه `dist/config` و فایل `.env` را به سرور خود منتقل کنید. به عنوان مثال، با استفاده از `scp`:
```bash
scp -r dist/config .env user@server:/path/to/project
```

#### 4. Install Docker / نصب داکر
On the server, install Docker and add your user to the Docker group:  
روی سرور، داکر را نصب کنید و کاربر خود را به گروه داکر اضافه کنید:
```bash
curl -fsSL https://get.docker.com -o install-docker.sh
sudo sh install-docker.sh
sudo usermod -aG docker $USER
```

#### 5. Create Docker Network / ایجاد شبکه داکر
Create a Docker network for the services:  
یک شبکه داکر برای سرویس‌ها ایجاد کنید:
```bash
docker network create --driver=bridge --subnet=10.0.0.0/16 edge
```
 

---

### Running the Project / اجرای پروژه
Navigate to the project directory on the server and start the services:  
به پوشه پروژه روی سرور بروید و سرویس‌ها را شروع کنید:
```bash
cd /path/to/project
docker compose down && docker compose up -d redis postgres synapse matrix web coturn sliding-sync
```

---

### Domains and Services / دامنه‌ها و سرویس‌ها
The project uses subdomains for different services:  
پروژه از زیر دامنه‌ها برای سرویس‌های مختلف استفاده می‌کند:
- `chat.V_MAIN_DOMAIN`: Main chat, Synapse, and Element / چت اصلی، Synapse و Element
- `to.chat.V_MAIN_DOMAIN`: Traefik dashboard / داشبورد Traefik
- `sync.chat.V_MAIN_DOMAIN`: Sliding sync service / سرویس همگام‌سازی اسلایدی
- `auth.chat.V_MAIN_DOMAIN`: Authentication service / سرویس احراز هویت
- `fed.s.chat.V_MAIN_DOMAIN`: Federation Synapse / فدراسیون Synapse
- `s.chat.V_MAIN_DOMAIN`: Synapse / Synapse
- `web.chat.V_MAIN_DOMAIN`: Element Web / وب Element

---


### Contributing / مشارکت
This project is open-source under the MIT license. Contributions are welcome! Please submit issues or pull requests on the repository.  
این پروژه متن‌باز تحت مجوز MIT است. مشارکت‌ها استقبال می‌شوند! لطفاً مشکلات یا درخواست‌های کشیدن را در مخزن ارسال کنید.

---

### License / مجوز
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  
این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات، فایل [LICENSE](LICENSE) را ببینید.



به امید روز های بهتر‌:)