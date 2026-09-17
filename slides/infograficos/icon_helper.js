const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

// Renders a react-icons component to a base64 PNG data string, ready for pptxgenjs addImage({data: ...})
async function iconToPngDataUrl(IconComponent, { color = "#FFFFFF", size = 512 } = {}) {
  const svgMarkup = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size })
  );
  const pngBuffer = await sharp(Buffer.from(svgMarkup))
    .resize(size, size)
    .png()
    .toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

module.exports = { iconToPngDataUrl };
