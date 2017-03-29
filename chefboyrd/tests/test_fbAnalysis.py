from chefboyrd.controllers import feedback_controller
from feedback_controller import feedback_analysis
from feedback_controller import word_freq_counter

""" Tests for correct performance of feedback analysis and word frequency counter on known string inputs.

"""

failStr = "Incorrect result for input \'{}\'"
testStr = "Food was good"
assert feedback_analysis(testStr) == [1,0,0,1,0], failStr.format(testStr)
testStr = "Service was bad"
assert feedback_analysis(testStr) == [0,1,0,0,1], failStr.format(testStr)
testStr = "Service was bad, but food was good"
assert feedback_analysis(testStr) == [1,1,1,1,1], failStr.format(testStr)

failStr2 = "Incorrect result for word frequency"
testStr2 = "bad bad bad"
result = word_freq_counter(testStr2)
assert [result[0]['text'],result[0]['size']] == ['bad',3], failStr2
testStr2 = "bad bad bad good good"
result = word_freq_counter(testStr2)
assert [result[0]['text'],result[0]['size']] == ['bad',3] or [result[0]['text'],result[0]['size']] == ['good',2], failStr2 
assert [result[1]['text'],result[1]['size']] == ['bad',3] or [result[1]['text'],result[1]['size']] == ['good',2], failStr2 
