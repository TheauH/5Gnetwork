#!/bin/bash

#Structure : test.sh whichUE whichTypeOFTest [Eventually other options]



# Check if there are no arguments
if [ $# -eq 0 ]; then
    echo "Usage: ./test.sh typeOfTest [otherInfoRequired]"
    echo "Please provide the necessary arguments for the test."
    exit 1
fi

# ---------------- To test tests -----------------------;
# Test case to check if the argument is "ok"
function test_ok_argument() {
    echo "Arguments : "$0" "$1" "$2""
    eval "./enter_container.sh ue2"
    if [ "$(pwd)" == "/UERANSIM/build" ]; then echo "Inside the container and at /UERANSIM/build"; fi
    if [ "$1" == "ok" ]; then
        echo "Test suite OK!"
    else
        echo "Problem with entering the container."
    fi
}


# ---------------- UE2 tests -----------------------;

# CONNECTION TEST


#check arguments
function test_case_1() { 
    echo "Running Test Case 1..."
    # run command ifconfig to check UE connections
    if [ "$1" == "connections" ] && { [ "$2" -eq 2 ] || [ "$2" -eq 4 ]; }; then
        echo "Test case for 'connections' argument passed!"
        # Call function to check uesimtun from 0 to 2 or 4 (depending on the second argument)
        check_uesimtun "$2"
    else
        echo "Test case for 'connections' argument failed!"
    fi

}
# Function to check uesimtun from 0 to 2 or 4
function check_uesimtun() {
    local max_value="$1"
    for i in $(seq 0 "$max_value"); do
        echo "Checking uesimtun$i..."
        ls | grep -q "uesimtun$i"
        if [ $? -eq 0 ]; then
            echo "OKAY: uesimtun$i found"
        else
            echo "ERROR: uesimtun$i not found"
        fi
    done
}





function test_case_2() {
    echo "Running Test Case 2..."
    # Add your test commands here
}




# ---------------- UE(1) tests -----------------------;









# ---------------- EXECUTION -----------------------;

# Main function to run tests
function run_tests() {
    echo "Starting tests..."
    # Call your test functions here
    #test_case_1
    #test_case_2
    test_ok_argument "$1"
    # Add more test cases as needed
    echo "All tests completed."
}


# Call the run_tests function when the script is executed with arguments
run_tests "$@"
