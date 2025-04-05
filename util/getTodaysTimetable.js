const { getAuthenticatedUntis } = require('./untisHelper');

async function getTodaysTimetable() {
    try {
        const untis = await getAuthenticatedUntis();
        const timetable = await untis.getOwnTimetableForToday();
        
        console.log('Gefundene Stunden:');
        console.table(timetable);
        
        return timetable;
    } catch (error) {
        console.error('Fehler in getTodaysTimetable:', error);
        throw error;
    }
}

// Expliziter Export
module.exports = getTodaysTimetable;