import * as helios from '@hyperionbt/helios'
import fs from 'fs'

const validatorSrc = fs.readFileSync('./vesting.helios').toString()

const validator = helios.Program.new(validatorSrc).compile()

fs.writeFileSync('./contract.json', validator.serialize())

const valHash = validator.validatorHash

console.log(validator.serialize())

console.log(helios.Address.fromValidatorHash(true, valHash).toBech32())
