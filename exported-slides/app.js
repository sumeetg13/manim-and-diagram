let ctx, canvas, slides = [], current = 0;

async function loadSlides() {
  const res = await fetch(SCENE_JSON_PATH);
  const json = await res.json();
  slides = json.frames;
  drawSlide(current);
}

function drawSlide(index) {
  if (!slides[index]) return;
  const frame = slides[index];
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (const obj of frame) {
    if (obj.type === "text") {
      ctx.font = `${obj.font_size || 24}px sans-serif`;
      ctx.fillStyle = obj.color || "black";
      ctx.fillText(obj.text, obj.x, obj.y);
    } else if (obj.type === "circle") {
      ctx.beginPath();
      ctx.arc(obj.x, obj.y, obj.radius || 30, 0, 2 * Math.PI);
      ctx.stroke();
    }
    // Add support for other objects here
  }
}

function nextSlide() {
  if (current < slides.length - 1) {
    current++;
    drawSlide(current);
  }
}

function prevSlide() {
  if (current > 0) {
    current--;
    drawSlide(current);
  }
}

window.onload = () => {
  canvas = document.getElementById("slide-canvas");
  canvas.width = 1280;
  canvas.height = 720;
  ctx = canvas.getContext("2d");
  loadSlides();
}
