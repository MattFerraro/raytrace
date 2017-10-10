import json


def dump(ray_history, fp):
    frames = [x.tolist() for x in ray_history]

    lines = []
    for i in xrange(len(frames[0])):
        lines.append([])

    for frame in frames:
        for i, point in enumerate(frame):
            lines[i].append(point)

    json.dump(lines, fp)


def dumps(ray_history):
    frames = [x.tolist() for x in ray_history]
    return json.dumps(frames)

def loads(string):
    print string
