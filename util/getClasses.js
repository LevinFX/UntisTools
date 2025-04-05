const { getAuthenticatedUntis } = require('./untisHelper');

async function getClasses() {
    try {
        const untis = await getAuthenticatedUntis();
        const classes = await untis.getClasses();
        
        console.log('Gefundene Klassen:');
        console.table(classes);
        
        return classes;
    } catch (error) {
        console.error('Fehler in getClasses:', error);
        throw error;
    }
}

// Expliziter Export
module.exports = getClasses;