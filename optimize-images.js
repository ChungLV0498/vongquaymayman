const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const inputDir = 'img';
const outputDir = 'img_webp';

// Create output directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
}

// Read all files from the input directory
fs.readdir(inputDir, (err, files) => {
    if (err) {
        console.error("Could not list the directory.", err);
        process.exit(1);
    }

    files.forEach((file, index) => {
        const inputPath = path.join(inputDir, file);
        const fileExt = path.extname(file).toLowerCase();

        // Process only jpg, jpeg, and png files
        if (['.jpg', '.jpeg', '.png'].includes(fileExt)) {
            const outputFileName = `${path.basename(file, fileExt)}.webp`;
            const outputPath = path.join(outputDir, outputFileName);

            sharp(inputPath)
                .resize({ width: 1920, withoutEnlargement: true }) // Resize to 1920px width max, don't enlarge smaller images
                .webp({ quality: 80 }) // Convert to webp with 80% quality
                .toFile(outputPath, (err, info) => {
                    if (err) {
                        console.error(`Error processing ${file}:`, err);
                    } else {
                        const originalSize = fs.statSync(inputPath).size / 1024 / 1024;
                        const newSize = info.size / 1024 / 1024;
                        console.log(`Processed ${file}: ${originalSize.toFixed(2)}MB -> ${newSize.toFixed(2)}MB`);
                    }
                });
        }
    });
});
