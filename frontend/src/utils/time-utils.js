export function getCurrentDateFormatted() {
    // Get the current date
    const today = new Date();

    // Extract day, month, and year
    let day = today.getDate();
    let month = today.getMonth() + 1; // Months are zero-based, so add 1
    let year = today.getFullYear();

    // Add leading zeros to day and month if they are less than 10
    day = day < 10 ? '0' + day : day;
    month = month < 10 ? '0' + month : month;

    // Format the date as DD-MM-YYYY
    const formattedDate = `${day}-${month}-${year}`;

    return formattedDate;
}

export function getCurrentMonthFormatted() {
    // Get the current date
    const today = new Date();

    // Extract month, and year
    let month = today.getMonth() + 1; // Months are zero-based, so add 1
    let year = today.getFullYear();

    // Add leading zeros to day and month if they are less than 10
    day = day < 10 ? '0' + day : day;
    month = month < 10 ? '0' + month : month;

    // Format the date as DD-MM-YYYY
    const formattedMonth = `${month}-${year}`;

    return formattedMonth;
}

// Functions takes in month in format "MM-YYYY" and converts to int
// E.g. convertFormattedMonthToInt("08-2024") returns 8
export function convertFormattedMonthToInt( formattedMonth ) {
    return parseInt(formattedMonth.slice(0, 2), 10);
}