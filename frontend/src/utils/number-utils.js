export function toNumber(val) {
    // parse strings like "SGD 5,000" or "32%" or "0.32" -> number
    if (val == null) return NaN;
    const n = Number(String(val).replace(/[^\d.-]/g, "")); // keep digits, dot, minus
    return Number.isFinite(n) ? n : NaN;
}