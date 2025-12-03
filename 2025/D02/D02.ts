import { readFileSync } from "node:fs"; 
console.log("AoC Day 02.");

// Now running node from parent directory.
// const inputText = readFileSync("./D02/sample_input", "utf8");
const inputText = readFileSync("./D02/input", "utf8");
const inputStrings = inputText.split(',');
// It appears that all the ranges are non-overlapping.

// Get all the ranges in number format.
type InputRange = {
    minNum: number,
    minStr: string,
    maxNum: number,
    maxStr: string,
    minDigits: number,
    maxDigits: number,
    evenDigitsArr?: number[]    // I am interested only in numbers with even number of digits for part 1.
};
let inputRanges: InputRange[] = [];

for (let rangeStr of inputStrings) {
    // Range strings in format ###-####. No negatives in ranges.
    let rangeNumsStr = rangeStr.split('-');
    let range: InputRange = {
        minNum: Number(rangeNumsStr[0]),
        minStr: rangeNumsStr[0],
        maxNum: Number(rangeNumsStr[1]),
        maxStr: rangeNumsStr[1],
        minDigits: rangeNumsStr[0].length,
        maxDigits: rangeNumsStr[1].length,
    }

    let evenDigitsArr: number[] = []
    for (let i = range.minDigits; i <= range.maxDigits; i++) {
        if (i % 2 === 0) {evenDigitsArr.push(i);}
    }
    range.evenDigitsArr = evenDigitsArr;
    
    inputRanges.push(range);    
}

// Part 1
let ans1 = 0;
// For each range, iterate over the even digits.
for (let range of inputRanges) {
    for (let digits of range.evenDigitsArr){
        let halfDigits = digits / 2;
        // Find the smallest possible invalid ID half in range.         
        let minInvalidHalf: number;
        if (digits > range.minStr.length) {
            minInvalidHalf = 10 ** (halfDigits - 1);
        }
        else {
            let frontSlice = Number(range.minStr.slice(0, halfDigits));
            let backSlice = Number(range.minStr.slice(halfDigits));
            minInvalidHalf = Math.max(
                frontSlice, 
                Math.min(
                    backSlice,
                    frontSlice + 1
                )
            );
        }

        // Find largest possible invalid ID half in range.
        let maxInvalidHalf: number;
        if (digits < range.maxStr.length) {
            maxInvalidHalf = Number("9".repeat(halfDigits))
        }
        else {
            let frontSlice = Number(range.maxStr.slice(0, halfDigits));
            let backSlice = Number(range.maxStr.slice(halfDigits));
            maxInvalidHalf = Math.min(
                frontSlice,
                Math.max(
                    backSlice,
                    frontSlice - 1
                )
            )
        }

        // Add invalid digit sum.
        if (minInvalidHalf <= maxInvalidHalf){
            let mid = (minInvalidHalf + maxInvalidHalf) / 2;
            let halfSum = mid * (maxInvalidHalf - minInvalidHalf + 1);
            let wholeSum = halfSum * 10 ** halfDigits + halfSum;
            ans1 += wholeSum;
        }
    }
}
console.log(`Part 1: ${ans1}`);

// Part 2
let ans2 = 0;
let primes = [2, 3, 5, 7, 11];
let invalidSet = new Set();
// For each range, check if there is a number of digits that will divide evenly by a prime.
// We don't check non primes because a prime factor will include the non-prime case.

type PrimeDividend = {prime: number, dividend: number}
for (let range of inputRanges){
    let primeDividends: PrimeDividend[] = [];
    for (let prime of primes){
        if (prime > range.maxDigits){break;}
        for (let i = range.minDigits; i <= range.maxDigits; i++) {
            if (i % prime === 0){
                primeDividends.push({prime: prime, dividend:i / prime});
            }
        }
    }
    // console.log(range, primeDividends);

    for (let pd of primeDividends) {
        // dividend is the number of digits in repeating unit.
        // prime is the number of repetitions of the unit.

        // get the smallest possible unit.
        let minInvalidUnit: number;
        let digits = pd.dividend * pd.prime;
        if (digits > range.minStr.length) {
            minInvalidUnit = 10 ** (pd.dividend - 1);
        }
        else {
            let frontSlice = Number(range.minStr.slice(0, pd.dividend));
            minInvalidUnit = frontSlice;
            for (let i = 1; i < pd.prime; i ++){
                let m = i * pd.dividend;
                let n = m + pd.dividend;
                let backSlice = Number(range.minStr.slice(m, n));

                if (backSlice > frontSlice){
                    minInvalidUnit = frontSlice + 1;
                    break;
                }
                if (backSlice < frontSlice){break;}
            }            
        }

        // get the largest possible unit.
        let maxInvalidUnit: number;
        if (digits < range.maxStr.length) {
            maxInvalidUnit = Number("9".repeat(pd.dividend))
        }
        else {
            let frontSlice = Number(range.maxStr.slice(0, pd.dividend));
            maxInvalidUnit = frontSlice;
            for (let i = 1; i < pd.prime; i ++){
                let m = i * pd.dividend;
                let n = m + pd.dividend;
                let backSlice = Number(range.maxStr.slice(m, n));

                if (backSlice < frontSlice){
                    maxInvalidUnit = frontSlice - 1;
                    break;
                }
                if (backSlice > frontSlice){break;}
            }
        }

        // Add invalid id sums. Sadly I have to resort back to iterating because of duplicate values such as 111111
        // which exist in multiple prime repetitions.
        for (let n = minInvalidUnit; n <= maxInvalidUnit; n++){
            let wholeNum = 0;
            for (let i = 0; i < pd.prime; i++){
                wholeNum += n * 10 ** (i * pd.dividend);
            }
            if (invalidSet.has(wholeNum)) {continue;}
            else {
                invalidSet.add(wholeNum);
                ans2 += wholeNum;
            }
        }
    }
}
console.log(`Part 2: ${ans2}`);
