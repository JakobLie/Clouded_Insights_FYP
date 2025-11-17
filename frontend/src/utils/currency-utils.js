export function formatCurrency(numberToFormat) {
    let isNegative = false;

    if (numberToFormat < 0) {
        isNegative = true;
        numberToFormat *= (-1);
        return "-"+numberToFormat.toLocaleString('en-US');
    }

    return numberToFormat.toLocaleString('en-US');
}