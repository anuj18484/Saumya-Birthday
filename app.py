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
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght=0,400;0,600;0,700;1,400&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <style>
        :root {
            --bg-dark: #0a0514;
            --glass-bg: rgba(255, 255, 255, 0.04);
            --glass-border: rgba(255, 255, 255, 0.1);
            --gold-light: #fcf6ba;
            --gold-dark: #bf953f;
            --rose-gold: #b76e79;
            --pink-glow: rgba(255, 105, 180, 0.35);
            --purple-glow: rgba(138, 43, 226, 0.25);
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
                radial-gradient(circle at 15% 50%, var(--purple-glow), transparent 30%),
                radial-gradient(circle at 85% 30%, var(--pink-glow), transparent 30%);
            background-attachment: fixed;
        }

        h1, h2, h3, .serif {
            font-family: 'Playfair Display', serif;
        }

        /* Utility Classes */
        .glass {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
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
            50% { transform: translateY(-20px) rotate(3deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }

        @keyframes pulse-glow {
            0% { box-shadow: 0 0 20px rgba(255, 105, 180, 0.3); transform: scale(1); }
            50% { box-shadow: 0 0 40px rgba(255, 105, 180, 0.7); transform: scale(1.02); }
            100% { box-shadow: 0 0 20px rgba(255, 105, 180, 0.3); transform: scale(1); }
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
            font-size: clamp(1.1rem, 2.5vw, 1.8rem);
            color: #ccc;
            letter-spacing: 3px;
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
            color: rgba(255, 255, 255, 0.25);
            font-size: 22px;
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
            width: 110px;
            height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: all 0.3s ease;
        }

        .time-box:hover {
            transform: translateY(-10px);
            border-color: var(--rose-gold);
            box-shadow: 0 10px 20px rgba(183, 110, 121, 0.2);
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
            max-width: 850px;
            text-align: center;
            padding: 4rem 1.5rem;
        }

        .typewriter-text {
            font-size: 1.4rem;
            line-height: 1.9;
            min-height: 180px;
            color: #eaeaea;
            font-weight: 400;
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
        .gallery-title-container {
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .gallery-subtitle {
            color: #b3b3b3;
            font-size: 1rem;
            margin-bottom: 2rem;
            letter-spacing: 1px;
        }

        .gallery-container {
            width: 100%;
            max-width: 1200px;
            display: flex;
            gap: 2rem;
            overflow-x: auto;
            padding: 2rem 1rem;
            scroll-snap-type: x mandatory;
            scrollbar-width: none;
        }
        
        .gallery-container::-webkit-scrollbar { display: none; }

        .gallery-card {
            min-width: 320px;
            height: 420px;
            border-radius: 24px;
            overflow: hidden;
            scroll-snap-align: center;
            position: relative;
            flex-shrink: 0;
            transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        }

        .gallery-card:hover {
            transform: scale(1.03) translateY(-5px);
        }

        .gallery-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.85;
            transition: opacity 0.3s, transform 0.5s ease;
        }

        .gallery-card:hover img {
            opacity: 1;
            transform: scale(1.05);
        }
        
        .gallery-caption {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 1.5rem;
            background: linear-gradient(transparent, rgba(0,0,0,0.85));
            color: #fff;
            font-size: 1rem;
            font-weight: 500;
        }

        /* Final Surprise */
        #surprise-section {
            text-align: center;
        }

        .surprise-btn {
            background: transparent;
            border: 2px solid var(--gold-dark);
            color: var(--gold-light);
            padding: 1.5rem 3.5rem;
            font-size: 1.4rem;
            border-radius: 50px;
            cursor: pointer;
            font-family: 'Poppins', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
            animation: pulse-glow 2.5s infinite;
        }

        .surprise-btn:hover {
            background: rgba(191, 149, 63, 0.15);
            border-color: #fff;
            color: #fff;
        }

        #final-message {
            display: none;
            max-width: 800px;
            margin-top: 3rem;
            padding: 3.5rem;
            opacity: 0;
            transition: opacity 2s ease-in;
            border: 1px solid rgba(255, 215, 0, 0.2);
            box-shadow: 0 0 50px rgba(191, 149, 63, 0.15);
        }

        #final-message p {
            font-size: 1.35rem;
            line-height: 2;
            color: #f0f0f0;
            margin-bottom: 1.5rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }

        /* Floating Music Controller */
        .music-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 65px;
            height: 65px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--rose-gold), var(--gold-dark));
            border: none;
            color: white;
            font-size: 1.6rem;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            z-index: 1000;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 8px 25px rgba(233, 30, 99, 0.4);
        }

        .music-btn:hover {
            transform: scale(1.15) rotate(10deg);
        }
        
        .music-pulse {
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: inherit;
            pointer-events: none;
            z-index: -1;
            opacity: 0.6;
            animation: musicRipple 2s infinite ease-out;
        }
        
        @keyframes musicRipple {
            0% { transform: scale(1); opacity: 0.6; }
            100% { transform: scale(1.6); opacity: 0; }
        }
    </style>
</head>
<body>

    <div class="particles" id="particles"></div>

    <button class="music-btn" id="musicToggle" onclick="toggleMusic()">
        <div class="music-pulse" id="pulseRing"></div>
        <i class="fas fa-play" id="musicIcon"></i>
    </button>
    
    <audio id="bgMusic" loop preload="auto">
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
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
        
        <a href="#special-message" style="position: absolute; bottom: 40px; color: white; opacity: 0.6; font-size: 2rem;" class="floating" aria-label="Scroll Down">
            <i class="fas fa-chevron-down"></i>
        </a>
    </section>

    <section id="special-message">
        <div class="glass" style="padding: 3.5rem 2rem; width: 100%;">
            <h2 class="serif text-gradient-gold" style="font-size: 2.5rem; margin-bottom: 2rem;">Dil Se Ek Baat... ✨</h2>
            <div class="typewriter-text">
                <span id="typed-text"></span><span class="cursor"></span>
            </div>
        </div>
    </section>

    <section id="gallery-section">
        <div class="gallery-title-container reveal">
            <h2 class="serif text-gradient-rose" style="font-size: 3rem;">Beautiful Memories</h2>
            <p class="gallery-subtitle">(Swipe ya scroll karke dekho 📸)</p>
        </div>
        
        <div class="gallery-container reveal">
            <div class="gallery-card glass">
                <img src="https://files.catbox.moe/sdbf1w.jpg" alt="Beautiful Lights and Celebrations">
                <div class="gallery-caption">Har pal khushiyon se bhara ho ✨</div>
            </div>
            <div class="gallery-card glass">
                <img src="https://files.catbox.moe/8i006r.jpg" alt="Joyful Moments">
                <div class="gallery-caption">Aapki smile sabsay pyari hai :)</div>
            </div>
            <div class="gallery-card glass">
                <img src="https://files.catbox.moe/83cz78.jpg" alt="Gold and Pink Decor">
                <div class="gallery-caption">Always the best sister in the world 🌍</div>
            </div>
            <div class="gallery-card glass">
                <img src="https://files.catbox.moe/8rq34r.jpg" alt="Gift Box Glitter">
                <div class="gallery-caption">Zindagi ki har khushi aapko mile 🎉</div>
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
            <h2 class="serif text-gradient-gold" style="font-size: 3rem; margin-bottom: 1.5rem;">Happy Birthday, Saumya! 🎂</h2>
            <p>Dear Saumya,</p>
            <p>Aap sirf meri behan nahi ho, balki meri zindagi ka sabsay bada aur sabsay keemti tohfa ho. Thank you hamesha mera saath dene ke liye aur mujhe samajhne ke liye.</p>
            <p>Main bhagwan se prarthana karta hoon ki aapko duniya ki saari khushi, kamyabi, acchi sehat aur behad khoobsurat memories milein.</p>
            <h3 class="text-gradient-rose" style="font-size: 2.2rem; margin-top: 2rem; font-family: 'Playfair Display', serif;">Aap hamesha aise hi muskurati raho ❤️</h3>
        </div>
    </section>

    <script>
        // 1. Particle Generator
        const particleChars = ['✨', '💖', '⭐', '💫', '🎈'];
        const particlesContainer = document.getElementById('particles');
        for(let i=0; i<30; i++) {
            let el = document.createElement('div');
            el.className = 'particle';
            el.innerText = particleChars[Math.floor(Math.random() * particleChars.length)];
            el.style.left = Math.random() * 100 + 'vw';
            el.style.top = Math.random() * 100 + 'vh';
            el.style.animationDuration = (Math.random() * 5 + 6) + 's';
            el.style.opacity = Math.random() * 0.4 + 0.3;
            particlesContainer.appendChild(el);
        }

        // 2. Countdown Logic (Target: August 4)
        function updateCountdown() {
            const now = new Date();
            let currentYear = now.getFullYear();
            let targetDate = new Date(currentYear, 7, 4); // 7 = August
            
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
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if(entry.isIntersecting) {
                    entry.target.classList.add('active');
                }
            });
        }, { threshold: 0.12 });
        reveals.forEach(reveal => revealObserver.observe(reveal));

        // 4. Hinglish Typewriter Effect
        const textToType = "Duniya ki sabsay awesome sister ko Happy Birthday! Aapke saath bitaya hua har lamha sabsay best hota hai. Aap ghar ki raunak ho aur meri sabsay acchi dost bhi. Aaj ka din aapke liye utna hi special ho jitni special aap mere liye ho! 🎉";
        let typedIndex = 0;
        let isTyping = false;
        
        const typeObserver = new IntersectionObserver((entries) => {
            if(entries[0].isIntersecting && !isTyping) {
                isTyping = true;
                setTimeout(typeText, 500);
            }
        }, { threshold: 0.4 });
        typeObserver.observe(document.getElementById('special-message'));

        function typeText() {
            if (typedIndex < textToType.length) {
                document.getElementById('typed-text').innerHTML += textToType.charAt(typedIndex);
                typedIndex++;
                setTimeout(typeText, 45);
            }
        }

         // 5. Music Play/Pause Fix (Ensured Connection)
        let musicPlaying = false;
        const bgMusic = document.getElementById('bgMusic');
        const musicIcon = document.getElementById('musicIcon');
        const pulseRing = document.getElementById('pulseRing');
        
        function toggleMusic() {
            if(musicPlaying) {
                bgMusic.pause();
                musicIcon.className = "fas fa-play";
                pulseRing.style.display = "none";
                musicPlaying = false;
            } else {
                bgMusic.play()
                    .then(() => {
                        musicIcon.className = "fas fa-pause";
                        pulseRing.style.display = "block";
                        musicPlaying = true;
                    })
                    .catch(e => {
                        console.log("Audio load error or gesture issue:", e);
                        alert("Please click anywhere on screen first, then try pressing play again!");
                    });
            }
        }

        // 6. Massive Surprise & Celebration
        function triggerSurprise() {
            document.getElementById('surprise-container').style.display = 'none';
            
            // Auto play music on surprise if not playing yet
            if(!musicPlaying) {
                toggleMusic();
            }

            const finalMsg = document.getElementById('final-message');
            finalMsg.style.display = 'block';
            setTimeout(() => finalMsg.style.opacity = '1', 100);

            // Grand Fireworks System
            const duration = 18 * 1000;
            const animationEnd = Date.now() + duration;
            const defaults = { startVelocity: 35, spread: 360, ticks: 70, zIndex: 1100 };

            function randomInRange(min, max) {
              return Math.random() * (max - min) + min;
            }

            const interval = setInterval(function() {
              const timeLeft = animationEnd - Date.now();

              if (timeLeft <= 0) {
                return clearInterval(interval);
              }

              const particleCount = 65 * (timeLeft / duration);
              
              confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.4), y: Math.random() - 0.2 } }));
              confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.6, 0.9), y: Math.random() - 0.2 } }));
            }, 300);
            
            // Blast on activation
            confetti({ particleCount: 200, spread: 200, origin: { y: 0.6 }, colors: ['#ffd700', '#ff6b6b', '#9b59b6', '#b76e79'] });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
