document.addEventListener('DOMContentLoaded', () => {
    const numberOfSnowflakes = 100;
    const snowContainer = document.createElement('div');
    snowContainer.className = 'snow';
    document.body.appendChild(snowContainer);

    for (let i = 0; i < numberOfSnowflakes; i++) {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        snowflake.textContent = '❄';
        snowflake.style.fontSize = `${Math.random() * 10 + 10}px`;
        snowflake.style.left = `${Math.random() * 100}vw`;
        snowflake.style.animationDuration = `${Math.random() * 10 + 10}s`;
        snowflake.style.animationDelay = `${Math.random() * 10}s`;
        snowflake.style.opacity = Math.random();
        snowflake.style.transform = `rotate(${Math.random() * 360}deg)`;
        snowContainer.appendChild(snowflake);
    }
});
