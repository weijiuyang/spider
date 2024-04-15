const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(StealthPlugin());

(async () => {
    // 启动浏览器
    const headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Referer": "https://www.v2ph.com/album/z7nnx65a.html?page=13&hl=zh-Hant",
        "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
    };

    const cookieString = "frontend=522f3e888be0c71ec97a55491bc15589; _ga=GA1.1.143578938.1712484793; cf_clearance=YZQr36.BnvNQWt7fp1BW5Ey83WeRJI7TtMV8At1Pt5E-1712484795-1.0.1.1-ss2GdojwhYjJ55SnQcCKKlEv4PgZvNUQUEyeSbzA50s.YjCdng6Mo_oq.Y.4PrCFMIXHX7f05QQ2HmHV304KRA; frontend-rmu=Cx31p%2FlO%2FqAr9rwoSCaQCi%2FgBfQFsA%3D%3D; frontend-rmt=R87hnzzcXFENUGjybaQ5BWz7D5rR5yCHGEgdegoiqmI%2B2C1coiBIc1Y0YvkbxLbw; _ga_170M3FX3HZ=GS1.1.1712484793.1.1.1712484939.60.0.0";
    const cookies = cookieString.split('; ').map(pair => {
        const [name, value] = pair.split('=');
        let domain;
        if (name.startsWith('f')) {
            domain = 'www.v2ph.com';
        } else {
            domain = '.v2ph.com';
        }
        return { name, value, domain };
        // return { name, value, domain: '.v2ph.com' }; // Adjust the domain accordingly
    });


    const browser = await puppeteer.launch({
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process', // 只有在Docker等环境中运行时才使用这个
            '--disable-gpu'
        ],
        headless: true
    });
    const page = await browser.newPage();

    await page.setExtraHTTPHeaders(headers);

    for (let cookie of cookies) {
        await page.setCookie(cookie);
    }

    await page.goto('https://www.v2ph.com/actor/8689xa7m.html?hl=zh-Hant');

    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await new Promise(resolve => setTimeout(resolve, 5000)); // 等待5000毫秒


    // 等待网络空闲或特定元素出现
    await page.waitForNetworkIdle();
    console.log(await page.content());
    await browser.close();

    // 关闭浏览器
    await browser.close();
})();
