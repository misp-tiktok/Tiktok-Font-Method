document.addEventListener('DOMContentLoaded', () => {
    const numberOfSnowflakes = 200; // Increase the number of snowflakes
    const snowContainer = document.createElement('div');
    snowContainer.className = 'snow';
    document.body.appendChild(snowContainer);

    for (let i = 0; i < numberOfSnowflakes; i++) {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        snowflake.style.fontSize = `${Math.random() * 10 + 10}px`; // Random size
        snowflake.style.left = `${Math.random() * 100}vw`; // Random horizontal position
        snowflake.style.animationDuration = `${Math.random() * 10 + 10}s`; // Random fall speed
        snowflake.style.animationDelay = `${Math.random() * 10}s`; // Random delay before falling
        snowflake.style.opacity = Math.random(); // Random opacity
        snowflake.style.transform = `rotate(${Math.random() * 360}deg)`; // Random rotation
        snowflake.textContent = '❄'; // Snowflake symbol
        snowContainer.appendChild(snowflake);
    }
});
