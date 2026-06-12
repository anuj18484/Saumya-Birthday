import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Happy Birthday Saumya</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <style>
        :root {
            --bg-dark: #0a0514;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.08);
            --gold-light: #fcf6ba;
            --gold-dark: #bf953f;
            --rose-gold: #b76e79;
            --pink-glow: rgba(255, 105, 180, 0.3);
            --purple-glow: rgba(138, 43, 226, 0.2);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            scroll-behavior: smooth;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background-color: var(--bg-dark);
            color: #ffffff;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 15% 50%, var(--purple-glow), transparent 25%),
                radial-gradient(circle at 85% 30%, var(--pink-glow), transparent 25%);
            background-attachment: fixed;
        }

        h1, h2, h3, .serif {
            font-family: 'Playfair Display', serif;
        }

        /* Utility Classes */
        .glass {
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }

        .text-gradient-gold {
            background: linear-gradient(to right, var(--gold-dark), var(--gold-light), var(--gold-dark));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% auto;
            animation: shine 3s linear infinite;
        }

        .text-gradient-rose {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Animations */
        @keyframes shine {
            to { background-position: 200% center; }
        }

        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(5deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }

        @keyframes pulse-glow {
            0% { box-shadow: 0 0 20px rgba(255, 105, 180, 0.2); }
            50% { box-shadow: 0 0 40px rgba(255, 105, 180, 0.6); }
            100% { box-shadow: 0 0 20px rgba(255, 105, 180, 0.2); }
        }

        .floating { animation: float 6s ease-in-out infinite; }
        .delay-1 { animation-delay: 1s; }
        .delay-2 { animation-delay: 2s; }

        .reveal {
            opacity: 0;
            transform: translateY(40px);
            transition: all 1s cubic-bezier(0.5, 0, 0, 1);
        }
        
        .reveal.active {
            opacity: 1;
            transform: translateY(0);
        }

        /* Sections */
        section {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2rem;
            position: relative;
        }

        /* Hero */
        #hero {
            text-align: center;
        }
        
        #hero h1 {
            font-size: clamp(3rem, 8vw, 6rem);
            line-height: 1.2;
            margin-bottom: 1rem;
            letter-spacing: 2px;
        }

        #hero p {
            font-size: clamp(1.2rem, 3vw, 2rem);
            color: #ccc;
            letter-spacing: 4px;
            text-transform: uppercase;
        }

        /* Floating Particles */
        .particles {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        }

        .particle {
            position: absolute;
            color: rgba(255, 255, 255, 0.2);
            font-size: 20px;
            animation: float 8s infinite linear;
        }

        /* Countdown */
        .countdown-container {
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 3rem;
        }

        .time-box {
            width: 100px;
            height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: transform 0.3s ease;
        }

        .time-box:hover {
            transform: translateY(-10px);
            border-color: var(--rose-gold);
        }

        .time-box span {
            font-size: 2.5rem;
            font-weight: 600;
            color: var(--gold-light);
        }

        .time-box p {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #aaa;
            margin-top: 0.5rem;
        }

        /* Typewriter Message */
        #special-message {
            max-width: 800px;
            text-align: center;
            padding: 4rem 2rem;
        }

        .typewriter-text {
            font-size: 1.5rem;
            line-height: 1.8;
            min-height: 150px;
            color: #eaeaea;
        }

        .cursor {
            display: inline-block;
            width: 3px;
            height: 1.5rem;
            background-color: var(--rose-gold);
            animation: blink 0.7s infinite;
            vertical-align: middle;
        }

        @keyframes blink { 50% { opacity: 0; } }

        /* Gallery */
        .gallery-container {
            width: 100%;
            max-width: 1200px;
            display: flex;
            gap: 2rem;
            overflow-x: auto;
            padding: 2rem 1rem;
            scroll-snap-type: x mandatory;
            scrollbar-width: none; /* Firefox */
        }
        
        .gallery-container::-webkit-scrollbar { display: none; } /* Chrome */

        .gallery-card {
            min-width: 300px;
            height: 400px;
            border-radius: 20px;
            overflow: hidden;
            scroll-snap-align: center;
            position: relative;
            flex-shrink: 0;
            transition: transform 0.4s;
        }

        .gallery-card:hover {
            transform: scale(1.05);
        }

        .gallery-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.8;
            transition: opacity 0.3s;
        }

        .gallery-card:hover img {
            opacity: 1;
        }

        /* Final Surprise */
        #surprise-section {
            text-align: center;
        }

        .surprise-btn {
            background: transparent;
            border: 2px solid var(--gold-dark);
            color: var(--gold-light);
            padding: 1.5rem 3rem;
            font-size: 1.5rem;
            border-radius: 50px;
            cursor: pointer;
            font-family: 'Poppins', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            animation: pulse-glow 2s infinite;
        }

        .surprise-btn:hover {
            background: rgba(191, 149, 63, 0.1);
            transform: scale(1.05);
        }

        #final-message {
            display: none;
            max-width: 800px;
            margin-top: 3rem;
            padding: 3rem;
            opacity: 0;
            transition: opacity 2s ease-in;
        }

        #final-message p {
            font-size: 1.4rem;
            line-height: 2;
            color: #fff;
            margin-bottom: 1.5rem;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
        }

        /* Music Controller */
        .music-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            color: white;
            font-size: 1.5rem;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            z-index: 1000;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        .music-btn:hover {
            transform: scale(1.1);
            background: rgba(255,255,255,0.1);
        }
    </style>
</head>
<body>

    <div class="particles" id="particles"></div>

    <button class="music-btn" id="musicToggle" onclick="toggleMusic()">
        <i class="fas fa-music"></i>
    </button>
    <audio id="bgMusic" loop>
        <source src="https://assets.mixkit.co/music/preview/mixkit-happy-birthday-to-you-piano-version-13.mp3" type="audio/mpeg">
    </audio>

    <section id="hero">
        <div class="reveal">
            <h1 class="text-gradient-gold floating">Happy Birthday<br><span class="text-gradient-rose">Saumya</span> ❤️</h1>
            <p class="floating delay-1">The Best Sister In My Life</p>
        </div>
        
        <div class="countdown-container reveal delay-2">
            <div class="time-box glass">
                <span id="days">00</span>
                <p>Days</p>
            </div>
            <div class="time-box glass">
                <span id="hours">00</span>
                <p>Hours</p>
            </div>
            <div class="time-box glass">
                <span id="minutes">00</span>
                <p>Minutes</p>
            </div>
            <div class="time-box glass">
                <span id="seconds">00</span>
                <p>Seconds</p>
            </div>
        </div>
        
        <a href="#special-message" style="position: absolute; bottom: 40px; color: white; opacity: 0.5; font-size: 2rem;" class="floating">
            <i class="fas fa-chevron-down"></i>
        </a>
    </section>

    <section id="special-message">
        <div class="glass" style="padding: 3rem; width: 100%;">
            <h2 class="serif text-gradient-gold" style="font-size: 2.5rem; margin-bottom: 2rem;">A Message For You</h2>
            <div class="typewriter-text">
                <span id="typed-text"></span><span class="cursor"></span>
            </div>
        </div>
    </section>

    <section id="gallery-section">
        <h2 class="serif text-gradient-rose reveal" style="font-size: 3rem; margin-bottom: 3rem; text-align: center;">Beautiful Memories</h2>
        <div class="gallery-container reveal">
            <div class="gallery-card glass">
                <img src="https://images.unsplash.com/photo-1513151233558-d860c5398176?w=600&q=80" alt="Celebration">
            </div>
            <div class="gallery-card glass">
                <img src="https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=600&q=80" alt="Flowers">
            </div>
            <div class="gallery-card glass">
                <img src="https://images.unsplash.com/photo-1558636508-e0db3814bd1d?w=600&q=80" alt="Cake">
            </div>
            <div class="gallery-card glass">
                <img src="https://images.unsplash.com/photo-1520854221256-17451cc331bf?w=600&q=80" alt="Lights">
            </div>
        </div>
    </section>

    <section id="surprise-section">
        <div class="reveal" id="surprise-container">
            <button class="surprise-btn" id="surpriseBtn" onclick="triggerSurprise()">
                Open Your Birthday Surprise 🎁
            </button>
        </div>

        <div id="final-message" class="glass">
            <h2 class="serif text-gradient-gold" style="font-size: 3rem; margin-bottom: 1rem;">Happy Birthday, Saumya!</h2>
            <p>Dear Saumya,</p>
            <p>You are not only my sister but also one of the most precious gifts in my life. Thank you for always being there for me.</p>
            <p>I wish you endless happiness, success, good health, and beautiful memories.</p>
            <h3 class="text-gradient-rose" style="font-size: 2rem; margin-top: 2rem;">I Love You ❤️</h3>
        </div>
    </section>

    <script>
        // 1. Particle Generator
        const particleChars = ['✨', '💖', '⭐', '💫', '🎈'];
        const particlesContainer = document.getElementById('particles');
        for(let i=0; i<25; i++) {
            let el = document.createElement('div');
            el.className = 'particle';
            el.innerText = particleChars[Math.floor(Math.random() * particleChars.length)];
            el.style.left = Math.random() * 100 + 'vw';
            el.style.top = Math.random() * 100 + 'vh';
            el.style.animationDuration = (Math.random() * 5 + 5) + 's';
            el.style.opacity = Math.random() * 0.5 + 0.2;
            particlesContainer.appendChild(el);
        }

        // 2. Countdown Logic (Target: Next August 4)
        function updateCountdown() {
            const now = new Date();
            let currentYear = now.getFullYear();
            let targetDate = new Date(currentYear, 7, 4); // Month is 0-indexed (7 = August)
            
            if (now.getTime() > targetDate.getTime()) {
                targetDate = new Date(currentYear + 1, 7, 4);
            }
            
            const diff = targetDate - now;
            
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
            const minutes = Math.floor((diff / 1000 / 60) % 60);
            const seconds = Math.floor((diff / 1000) % 60);
            
            document.getElementById('days').innerText = days.toString().padStart(2, '0');
            document.getElementById('hours').innerText = hours.toString().padStart(2, '0');
            document.getElementById('minutes').innerText = minutes.toString().padStart(2, '0');
            document.getElementById('seconds').innerText = seconds.toString().padStart(2, '0');
        }
        setInterval(updateCountdown, 1000);
        updateCountdown();

        // 3. Scroll Reveal Observer
        const reveals = document.querySelectorAll('.reveal');
        const revealOptions = { threshold: 0.15 };
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if(entry.isIntersecting) {
                    entry.target.classList.add('active');
                }
            });
        }, revealOptions);
        reveals.forEach(reveal => revealObserver.observe(reveal));

        // 4. Typewriter Effect
        const textToType = "To the most amazing sister in the world. Growing up with you has been the greatest adventure. You bring so much light, laughter, and joy into every single day. Here is to celebrating YOU! 🎉";
        let typedIndex = 0;
        let isTyping = false;
        
        const typeObserver = new IntersectionObserver((entries) => {
            if(entries[0].isIntersecting && !isTyping) {
                isTyping = true;
                typeText();
            }
        }, { threshold: 0.5 });
        typeObserver.observe(document.getElementById('special-message'));

        function typeText() {
            if (typedIndex < textToType.length) {
                document.getElementById('typed-text').innerHTML += textToType.charAt(typedIndex);
                typedIndex++;
                setTimeout(typeText, 40);
            }
        }

        // 5. Music Toggle
        let musicPlaying = false;
        const bgMusic = document.getElementById('bgMusic');
        const musicBtn = document.getElementById('musicToggle');
        
        function toggleMusic() {
            if(musicPlaying) {
                bgMusic.pause();
                musicBtn.innerHTML = '<i class="fas fa-music"></i>';
                musicPlaying = false;
            } else {
                bgMusic.play().catch(e => console.log("Audio play prevented by browser"));
                musicBtn.innerHTML = '<i class="fas fa-pause"></i>';
                musicPlaying = true;
            }
        }

        // 6. Final Surprise & Fireworks
        function triggerSurprise() {
            // Hide button
            document.getElementById('surprise-container').style.display = 'none';
            
            // Show Message
            const finalMsg = document.getElementById('final-message');
            finalMsg.style.display = 'block';
            setTimeout(() => finalMsg.style.opacity = '1', 100);

            // Realistic Fireworks using canvas-confetti
            const duration = 15 * 1000;
            const animationEnd = Date.now() + duration;
            const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

            function randomInRange(min, max) {
              return Math.random() * (max - min) + min;
            }

            const interval = setInterval(function() {
              const timeLeft = animationEnd - Date.now();

              if (timeLeft <= 0) {
                return clearInterval(interval);
              }

              const particleCount = 50 * (timeLeft / duration);
              
              // Fire from multiple locations
              confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
              confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
            }, 250);
            
            // Initial blast
            confetti({ particleCount: 150, spread: 180, origin: { y: 0.6 }, colors: ['#ffd700', '#ff6b6b', '#9b59b6'] });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    # Configured for GitHub and Render (uses environment PORT if available, defaults to 5000)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
  
