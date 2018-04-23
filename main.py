import sys
import sequential
import fromKenlist
import tags


if __name__ == '__main__':

    rule_1 = []
    rule_2 = []
    rule_3 = []

    video_id = raw_input()

    rule_1 = tags.tags(video_id)
    rule_2 = fromKenlist.fromKenlist(video_id)
    rule_3 = sequential.sequential(video_id)
    
    print rule_1, rule_2, rule_3
