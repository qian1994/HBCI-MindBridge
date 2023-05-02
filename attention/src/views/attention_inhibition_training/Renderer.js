class Renderer {
    constructor(ctx, unitWidth, unitHeight, offsetLeft, offsetTop) {
      this.ctx = ctx;
      this.unitWidth = unitWidth;
      this.unitHeight = unitHeight;
      this.offsetLeft = offsetLeft;
      this.offsetTop = offsetTop;
      this.wallWidth = 2;
    }
  
    clear(w, h) {
      this.ctx.clearRect(0, 0, w, h);
    }
  
    setColor(fill, stroke) {
      this.ctx.fillStyle = fill;
      this.ctx.strokeStyle = stroke;
    }
  
    beginPath() {
      this.ctx.beginPath();
    }
  
    stroke() {
      this.ctx.stroke();
    }
  
    drawImage(x, y, image) {
      const scaleX = this.unitWidth / image.width;
      const scaleY = this.unitHeight / image.height;
      const cx = (x * this.unitWidth) / scaleX + this.offsetLeft / scaleX;
      const cy = (y * this.unitHeight) / scaleY + this.offsetTop / scaleY;
      this.ctx.save();
      this.ctx.scale(scaleX, scaleY);
      this.ctx.imageSmoothingEnabled = false;
      this.ctx.drawImage(image, cx, cy);
      this.ctx.restore();
    }
  
    drawCircle(x, y, r) {
      this.ctx.beginPath();
      const cx = x * this.unitWidth + this.unitWidth / 2 + this.offsetLeft;
      const cy = y * this.unitHeight + this.unitHeight / 2 + this.offsetTop;
      r =
        r != null
          ? r
          : Math.min(this.unitWidth, this.unitHeight) / 2 - this.wallWidth;
      this.ctx.arc(cx, cy, r, 0, 2 * Math.PI);
      this.ctx.fill();
      this.ctx.stroke();
    }
  
    drawLine(x1, y1, x2, y2) {
      const fromX = this.offsetLeft + x1 * this.unitWidth;
      const fromY = this.offsetTop + y1 * this.unitHeight;
      const toX = this.offsetLeft + x2 * this.unitWidth;
      const toY = this.offsetTop + y2 * this.unitHeight;
      this.ctx.moveTo(fromX, fromY);
      this.ctx.lineTo(toX, toY);
    }
  
    drawText(text, x, y) {
      const left = x * this.unitWidth + this.offsetLeft;
      const top = y * this.unitHeight + this.offsetTop;
      this.ctx.fillStyle = "black";
      this.ctx.fillText(text, left, top);
    }
  }
  
  export default Renderer;