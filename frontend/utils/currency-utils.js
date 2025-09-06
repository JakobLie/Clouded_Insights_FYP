export function formatCurrency(numberToFormat) {
    numberToFormat = numberToFormat < 0 ? -numberToFormat : numberToFormat;
    return numberToFormat.toLocaleString('en-US');
}