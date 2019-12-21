# boundary_check
given a polygon and a point verifies if the point lies within the polygon or not

## run command
```py
python routes.py
```
## sample requests

createCity

```json
{
    "name": "a",
    "boundaries": {"coords":[[0, 0], [0, 2], [2, 4], [3, 4], [3, 1]]}
}
```

checkBoundary

```json
{
    "name": "a",
    "point": {"coords":{"x": 2,"y": 2}}
}
```
