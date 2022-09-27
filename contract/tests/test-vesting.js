import * as helios from '@hyperionbt/helios'
import assert from 'assert'
import fs from 'fs'


const validator = fs.readFileSync("../vesting.helios").toString()
const testParams = fs.readFileSync("./test-params.helios").toString()
// Concat validator src and test params src
const program = helios.Program.new(validator + testParams)

/**
 * @param {paramNames} []string
 */
async function testDeadlinePassedSignedByBeneficiary(paramNames) {
    console.log("Test: testDeadlinePassedSignedByBeneficiary")

    const args = paramNames.map(p => program.evalParam(p))

    console.log("ARGS: ", args.map(v => v.toString()))

    const output = await program
        .compile()
        .runWithPrint(args)

    console.log(output[1])
    const returnValue = output[0]
    console.log(returnValue.toString())
    assert(returnValue.toString() == "()")
    console.log("Test `testDeadlinePassedSignedByBeneficiary` was successful.\n")
}

async function testDeadlineNotPassedSignedByBeneficiary(paramNames) {
    console.log("Test: testDeadlineNotPassedSignedByBeneficiary")

    const args = paramNames.map(p => program.evalParam(p))

    console.log("ARGS: ", args.map(v => v.toString()))

    const output = await program
        .compile()
        .runWithPrint(args)

    console.log(output[1])
    const returnValue = output[0]
    console.log(returnValue.info)
    assert(returnValue instanceof helios.UserError) 
    assert(returnValue.info == "transaction rejected")
    console.log("Test `testDeadlineNotPassedSignedByBeneficiary` was successful.\n")
}


await testDeadlinePassedSignedByBeneficiary(
    ["test1_datum", "test1_redeemer", "test1_ctx"]
)

await testDeadlineNotPassedSignedByBeneficiary(
    ["test2_datum", "test2_redeemer", "test2_ctx"]
)
