const { getAuthenticatedUntis } = require('./untisHelper');

module.exports = async function getStudents() {
    try {
        const untis = await getAuthenticatedUntis();
        const students = await untis.getStudents();
            
        return students;
    } catch (error) {
        console.error('Fehler in getStudents:', error);
        throw error;
    }
};