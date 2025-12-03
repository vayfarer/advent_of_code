import { readFileSync } from "node:fs"; 
console.log("AoC Day 01.");

// const inputText = readFileSync("./sample_input", "utf8");
const inputText = readFileSync("./input", "utf8");
const inputLines = inputText.split('\n');
let inputNums: number[] = [];

for (let numStr of inputLines) {
    // presumably all input lines are in the format "X#", 1 character L or R, remaining chars number.
    let sign = numStr[0] === 'R' ? 1 : -1;
    let num = Number(numStr.slice(1)) * sign;
    inputNums.push(num);    
}

// part 1
let ans1 = 0;
let val = 50;
for (let num of inputNums){
    val += num;
    val = val % 100;
    if (val === 0) {
        ans1 += 1;
    }
}
console.log(`Part 1: ${ans1}`);

// part 2
val = 50;
let ans2 = 0;
for (let num of inputNums){
    let oldVal = val;
    val += num;
    let revs = Math.abs(Math.trunc(val / 100));
    if (val < 0 && oldVal > 0 || num < 0 && val === 0){
        revs += 1;   // crossed or landed on zero going negative from initial positive value.
    }
    ans2 += revs;
    val = val % 100;
    if (val < 0 ){
        val = val + 100;
    }
}
console.log(`Part 2: ${ans2}`);

