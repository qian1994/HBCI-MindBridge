class Maze {
    constructor(lx, ly) {
        const bondHSize = (lx + 1) * ly;
        const bondVSize = lx * (ly + 1);
        const pointSize = lx * ly;
        const bondH = new Array(bondHSize).fill(false);
        const bondV = new Array(bondVSize).fill(false);
        const isOpenArr = new Array(pointSize).fill(false);

        this.lx = lx;
        this.ly = ly;
        this.bondH = bondH;
        this.bondV = bondV;
        this.isOpenArr = isOpenArr;

        this.makeMaze();
        this.goal = {
            x: this.lx - 1,
            y: this.ly - 1,
        };
    }

    makeMaze() {
        const cells = [];
        cells.push(Math.floor(Math.random() * this.isOpenArr.length));

        while (cells.length > 0) {
            const c = cells.pop();
            if (c == null) {
                break;
            }
            const ix = c % this.lx;
            const iy = Math.floor(c / this.lx);
            this.isOpenArr[c] = true;
            const direction = this.getDirectionCandidate(ix, iy);
            if (this.isDeadEnd(direction)) {
                continue;
            }
            cells.push(c);
            const dest = this.getNeighbor(ix, iy, this.getRandomDirection(direction));
            cells.push(dest.iy * this.lx + dest.ix);
        }

        this.bondH[0] = true;
        this.bondH[(this.lx + 1) * this.ly - 1] = true;
        return;
    }

    isDeadEnd(direction) {
        return (
            direction.north === 0 &&
            direction.south === 0 &&
            direction.west === 0 &&
            direction.east === 0
        );
    }

    isOpen(x, y) {
        return this.isOpenArr[y * this.lx + x];
    }

    getDirectionCandidate(ix, iy) {
        const north = iy > 0 && !this.isOpen(ix, iy - 1);
        const south = iy < this.ly - 1 && !this.isOpen(ix, iy + 1);
        const west = ix > 0 && !this.isOpen(ix - 1, iy);
        const east = ix < this.lx - 1 && !this.isOpen(ix + 1, iy);
        const directionNo = [north, south, west, east].filter((i) => i).length;
        const probability = directionNo > 0 ? 1.0 / directionNo : 0;
        return {
            north: north ? probability : 0,
            south: south ? probability : 0,
            west: west ? probability : 0,
            east: east ? probability : 0,
        };
    }

    getRandomDirection(direction) {
        const sum =
            direction.north + direction.south + direction.west + direction.east;
        if (sum === 0) {
            throw new Error("No direction available");
        }
        const i = Math.random() * sum;
        let n = 0;
        for (const k in direction) {
            const p = direction[k];
            n += p;
            if (i < n) {
                return k;
            }
        }
        throw new Error("Something wrong");
    }

    getNeighbor(ix, iy, direction) {
        const dest = { ix, iy };
        switch (direction) {
            case "north":
                dest.iy -= 1;
                this.bondV[iy * this.lx + ix] = true;
                break;
            case "south":
                dest.iy += 1;
                this.bondV[(iy + 1) * this.lx + ix] = true;
                break;
            case "east":
                dest.ix += 1;
                this.bondH[iy * (this.lx + 1) + ix + 1] = true;
                break;
            case "west":
                dest.ix -= 1;
                this.bondH[iy * (this.lx + 1) + ix] = true;
                break;
            default:
                throw new Error("Something wrong");
        }
        return dest;
    }
}

export default Maze;
