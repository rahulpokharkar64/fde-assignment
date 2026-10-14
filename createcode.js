const fs = require('fs/promises');
const path = require('path');

async function createSyllabusFolders() {
  const totalWeeks = 16;
  const daysPerWeek = 2;
  
  // Base directory where you want to create these folders (current directory)
  const baseDir = __dirname;

  try {
    for (let w = 1; w <= totalWeeks; w++) {
      const weekFolderName = `Week${w}`;
      
      for (let d = 1; d <= daysPerWeek; d++) {
        // String.prototype.padStart ensures "1" becomes "01", "2" becomes "02"
        const dayFolderName = `Day${String(d).padStart(2, '0')}`;
        
        // Construct the full nested path: e.g., ./Week1/Day 01
        const targetPath = path.join(baseDir, weekFolderName, dayFolderName);
        
        // fs.mkdir with { recursive: true } automatically creates parent folders (like Week1) if they don't exist
        await fs.mkdir(targetPath, { recursive: true });
      }
    }
    console.log('✅ Successfully created folders from Week1 to Week 16 with Day 01 and Day 02 subgroups!');
  } catch (error) {
    console.error('❌ Error creating folders:', error);
  }
}

createSyllabusFolders();
