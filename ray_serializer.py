import json


def dump(all_ray_histories, fp):

    serialized = []

    for history, color in all_ray_histories:

        frames = [x.tolist() for x in history]

        lines = []
        for i in xrange(len(frames[0])):
            lines.append([])

        for frame in frames:
            for i, point in enumerate(frame):
                lines[i].append(point)

        serialized.append((lines, color))

    json.dump(serialized, fp)


def dumps(ray_history):
    frames = [x.tolist() for x in ray_history]
    return json.dumps(frames)

def loads(string):
    print string
