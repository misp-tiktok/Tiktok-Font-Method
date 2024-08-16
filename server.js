const express = require('express');
const puppeteer = require('puppeteer');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());
app.use(express.static('public')); // Serve static files

app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto('https://www.tiktok.com/login');

        // Perform login
        await page.type('input[name="username"]', username);
        await page.type('input[name="password"]', password);
        await page.click('button[type="submit"]');

        // Wait for navigation or necessary page state
        await page.waitForNavigation();

        // Extract session ID from cookies or local storage
        const cookies = await page.cookies();
        const sessionIdCookie = cookies.find(cookie => cookie.name === 'sessionid');

        await browser.close();

        if (sessionIdCookie) {
            res.json({ sessionId: sessionIdCookie.value });
        } else {
            res.status(400).json({ error: 'Session ID not found.' });
        }
    } catch (error) {
        console.error('Error during login:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
