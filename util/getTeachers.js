const { getAuthenticatedUntis } = require('./untisHelper');

module.exports = async function getTeachers() {
    try {
        const untis = await getAuthenticatedUntis();
        const students = await untis.getTeachers();
            
        return students;
    } catch (error) {
        console.error('Fehler in getTeachers:', error);
        throw error;
    }
};