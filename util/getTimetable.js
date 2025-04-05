const { getAuthenticatedUntis } = require('./untisHelper');

module.exports = async function getTimetable(classId, date = new Date()) {
    try {
        const untis = await getAuthenticatedUntis();
        const timetable = await untis.getOwnTimetableForWeek(date, classId);
        
        
        console.log(`Stundenplan für ${date.toLocaleDateString()}:`);
        console.table(timetable);
        
        return timetable;
    } catch (error) {
        console.error('Fehler in getTimetable:', error);
        throw error;
    }
};