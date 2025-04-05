const { getAuthenticatedUntis } = require('./untisHelper');

async function getAbsentLessons(startDate = new Date(), endDate = new Date()) {
    try {
        let today = new Date();
        const end = new Date();
        const start = new Date();
        end.setDate(today.getDate()+5)
        start.setDate(today.getDate()-100)

        const untis = await getAuthenticatedUntis();
        const lessons = await untis.getAbsentLesson(start,end);
        
        console.log('Gefunden:');
        console.table(lessons);
        
        return lessons;
    } catch (error) {
        console.error('Fehler in getAbsentLessons:', error);
        throw error;
    }
}

// Expliziter Export
module.exports = getAbsentLessons;