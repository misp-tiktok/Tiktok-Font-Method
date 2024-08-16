const puppeteer = require('puppeteer');

(async () => {
    // Launch a new browser instance
    const browser = await puppeteer.launch({ headless: false }); // Set headless to false to see the browser window
    const page = await browser.newPage();

    // Navigate to TikTok login page
    await page.goto('https://www.tiktok.com/login');

    // Fill in login credentials (Replace with your TikTok credentials)
    await page.type('input[name="username"]', 'your-username'); // Update this selector as necessary
    await page.type('input[name="password"]', 'your-password'); // Update this selector as necessary

    // Click the login button
    await page.click('button[type="submit"]'); // Update this selector as necessary

    // Wait for the navigation or required page state
    await page.waitForNavigation({ waitUntil: 'networkidle2' });

    // Wait for a short period to ensure any CAPTCHA or 2SV is handled
    await page.waitForTimeout(10000); // Increase if needed

    // Extract cookies
    const cookies = await page.cookies();
    const sessionIdCookie = cookies.find(cookie => cookie.name === 'sessionid'); // Adjust cookie name if needed

    if (sessionIdCookie) {
        console.log('Session ID:', sessionIdCookie.value);
    } else {
        console.log('Session ID not found.');
    }

    // Close the browser
    await browser.close();
})();
