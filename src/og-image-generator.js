/**
 * OG Image Generator für Social Media
 * Generiert dynamische Open Graph Bilder für maximales Engagement
 */

function generateOGImageMeta(article, category) {
  // Generiert Open Graph Meta Tags für einzelne Artikel
  const ogImage = `/api/og-image?title=${encodeURIComponent(article.title)}&category=${category}`;
  
  return {
    title: article.title,
    description: article.description || article.title,
    image: ogImage,
    imageAlt: article.title,
    keywords: article.keywords || ""
  };
}

// Express.js Endpoint (wenn Backend vorhanden ist)
function setupOGImageAPI(app) {
  app.get('/api/og-image', (req, res) => {
    const { title, category } = req.query;
    
    // Nutzt Canvas um dynamisches OG Bild zu generieren
    const canvas = require('canvas').createCanvas(1200, 630);
    const ctx = canvas.getContext('2d');
    
    // Background Gradient
    const gradient = ctx.createLinearGradient(0, 0, 1200, 630);
    gradient.addColorStop(0, '#217c3b');
    gradient.addColorStop(1, '#156b2a');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 1200, 630);
    
    // Category Badge
    ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.fillRect(40, 40, 200, 50);
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 20px Arial';
    ctx.fillText(category || 'Faktencheck', 60, 75);
    
    // Title Text
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 42px Arial';
    ctx.lineWidth = 5;
    
    // Wrap title text
    const maxWidth = 1100;
    const words = title.split(' ');
    let line = '';
    let y = 150;
    
    words.forEach(word => {
      const testLine = line + word + ' ';
      const metrics = ctx.measureText(testLine);
      
      if (metrics.width > maxWidth) {
        ctx.fillText(line, 50, y);
        line = word + ' ';
        y += 60;
      } else {
        line = testLine;
      }
    });
    ctx.fillText(line, 50, y);
    
    // Footer
    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.fillRect(0, 550, 1200, 80);
    ctx.fillStyle = '#fff';
    ctx.font = '20px Arial';
    ctx.fillText('Grüner Faktencheck - Unabhängige Analysen', 50, 590);
    ctx.fillText('gruener-faktencheck.de', 50, 620);
    
    // Send image
    res.type('image/png');
    canvas.pngStream().pipe(res);
  });
}

export { generateOGImageMeta, setupOGImageAPI };
