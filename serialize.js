import * as helios from '@hyperionbt/helios'
import fs from 'fs'

const validator = fs.readFileSync('./vesting.helios').toString()

const serializedValidator = helios.Program.new(validator).compile(true).serialize()

console.log(serializedValidator)

fs.writeFileSync('./contract.json', serializedValidator)
