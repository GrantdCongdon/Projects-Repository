import java.util.ArrayList;
import java.util.Random;
import java.util.concurrent.TimeUnit;
import java.util.Scanner;
class box {
		box north; box south; box east; box west; int x; int y; int wallNumber;
		boolean northWall, southWall, eastWall, westWall;
		String value = new String();
		public box (box north, box south, box east, box west) {
				Random w = new Random();
				this.north = north;
				this.south = south;
				this.east = east;
				this.west = west;
				this.wallNumber = 0;
				if (west==null) { this.x=0; this.westWall=true; }
				else { this.x = 1+west.x; }
				if (north==null) { this.y=0; this.northWall=true; }
				else {this.y = 1+north.y; }
				if (east==null) { this.eastWall=true; }
				if (south==null) { this.southWall=true; }
				
				if (northWall && southWall && eastWall && westWall) { value = "A   "; wallNumber = 4; }
				
				else if (!northWall && southWall && eastWall && westWall) { value = "SEW "; wallNumber = 3; }
				else if (northWall && !southWall && eastWall && westWall) { value = "NEW "; wallNumber = 3; }
				else if (northWall && southWall && !eastWall && westWall) { value = "NSW "; wallNumber = 3; }
				else if (northWall && southWall && eastWall && !westWall) { value = "NSE "; wallNumber = 3; }
				
				else if (!northWall && !southWall && eastWall && westWall) { value = "WE  "; wallNumber = 2; }
				else if (!northWall && southWall && !eastWall && westWall) { value = "SW  "; wallNumber = 2; }
				else if (!northWall && southWall && eastWall && !westWall) { value = "SE  "; wallNumber = 2; }
				
				else if (northWall && !southWall && !eastWall && westWall) { value = "NW  "; wallNumber = 2; }
				else if (northWall && !southWall && eastWall && !westWall) { value = "NE  "; wallNumber = 2; }
				
				else if (northWall && southWall && !eastWall && !westWall) { value = "NS  "; wallNumber = 2; }
				
				else if (northWall && !southWall && !eastWall && !westWall) { value = "N   "; wallNumber = 1; }
				else if (!northWall && southWall && !eastWall && !westWall) { value = "S   "; wallNumber = 1; }
				else if (!northWall && !southWall && eastWall && !westWall) { value = "E   "; wallNumber = 1; }
				else if (!northWall && !southWall && !eastWall && westWall) { value = "W   "; wallNumber = 1; }
				
				else if (!northWall && !southWall && !eastWall && !westWall) { value = "    "; wallNumber = 0; }
		}
		void setNorthWall(boolean state) {
				this.northWall = state;
				
				if (northWall && southWall && eastWall && westWall) { value = "A   "; wallNumber = 4; }
				
				else if (!northWall && southWall && eastWall && westWall) { value = "SEW "; wallNumber = 3; }
				else if (northWall && !southWall && eastWall && westWall) { value = "NEW "; wallNumber = 3; }
				else if (northWall && southWall && !eastWall && westWall) { value = "NSW "; wallNumber = 3; }
				else if (northWall && southWall && eastWall && !westWall) { value = "NSE "; wallNumber = 3; }
				
				else if (!northWall && !southWall && eastWall && westWall) { value = "WE  "; wallNumber = 2; }
				else if (!northWall && southWall && !eastWall && westWall) { value = "SW  "; wallNumber = 2; }
				else if (!northWall && southWall && eastWall && !westWall) { value = "SE  "; wallNumber = 2; }
				
				else if (northWall && !southWall && !eastWall && westWall) { value = "NW  "; wallNumber = 2; }
				else if (northWall && !southWall && eastWall && !westWall) { value = "NE  "; wallNumber = 2; }
				
				else if (northWall && southWall && !eastWall && !westWall) { value = "NS  "; wallNumber = 2; }
				
				else if (northWall && !southWall && !eastWall && !westWall) { value = "N   "; wallNumber = 1; }
				else if (!northWall && southWall && !eastWall && !westWall) { value = "S   "; wallNumber = 1; }
				else if (!northWall && !southWall && eastWall && !westWall) { value = "E   "; wallNumber = 1; }
				else if (!northWall && !southWall && !eastWall && westWall) { value = "W   "; wallNumber = 1; }
				
				else if (!northWall && !southWall && !eastWall && !westWall) { value = "    "; wallNumber = 0; }
		}
		void setSouthWall(boolean state) {
				this.southWall = state;
				if (northWall && southWall && eastWall && westWall) { value = "A   "; wallNumber = 4; }
				
				else if (!northWall && southWall && eastWall && westWall) { value = "SEW "; wallNumber = 3; }
				else if (northWall && !southWall && eastWall && westWall) { value = "NEW "; wallNumber = 3; }
				else if (northWall && southWall && !eastWall && westWall) { value = "NSW "; wallNumber = 3; }
				else if (northWall && southWall && eastWall && !westWall) { value = "NSE "; wallNumber = 3; }

				else if (!northWall && !southWall && eastWall && westWall) { value = "WE  "; wallNumber = 2; }
				else if (!northWall && southWall && !eastWall && westWall) { value = "SW  "; wallNumber = 2; }
				else if (!northWall && southWall && eastWall && !westWall) { value = "SE  "; wallNumber = 2; }
				
				else if (northWall && !southWall && !eastWall && westWall) { value = "NW  "; wallNumber = 2; }
				else if (northWall && !southWall && eastWall && !westWall) { value = "NE  "; wallNumber = 2; }
				
				else if (northWall && southWall && !eastWall && !westWall) { value = "NS  "; wallNumber = 2; }
				
				else if (northWall && !southWall && !eastWall && !westWall) { value = "N   "; wallNumber = 1; }
				else if (!northWall && southWall && !eastWall && !westWall) { value = "S   "; wallNumber = 1; }
				else if (!northWall && !southWall && eastWall && !westWall) { value = "E   "; wallNumber = 1; }
				else if (!northWall && !southWall && !eastWall && westWall) { value = "W   "; wallNumber = 1; }
				
				else if (!northWall && !southWall && !eastWall && !westWall) { value = "    "; wallNumber = 0; }
		}
		void setEastWall(boolean state) {
				this.eastWall = state;
				if (northWall && southWall && eastWall && westWall) { value = "A    "; wallNumber = 4; }
				
				else if (!northWall && southWall && eastWall && westWall) { value = "SEW "; wallNumber = 3; }
				else if (northWall && !southWall && eastWall && westWall) { value = "NEW "; wallNumber = 3; }
				else if (northWall && southWall && !eastWall && westWall) { value = "NSW "; wallNumber = 3; }
				else if (northWall && southWall && eastWall && !westWall) { value = "NSE "; wallNumber = 3; }

				else if (!northWall && !southWall && eastWall && westWall) { value = "WE  "; wallNumber = 2; }
				else if (!northWall && southWall && !eastWall && westWall) { value = "SW  "; wallNumber = 2; }
				else if (!northWall && southWall && eastWall && !westWall) { value = "SE  "; wallNumber = 2; }
				
				else if (northWall && !southWall && !eastWall && westWall) { value = "NW  "; wallNumber = 2; }
				else if (northWall && !southWall && eastWall && !westWall) { value = "NE  "; wallNumber = 2; }
				
				else if (northWall && southWall && !eastWall && !westWall) { value = "NS  "; wallNumber = 2; }
				
				else if (northWall && !southWall && !eastWall && !westWall) { value = "N   "; wallNumber = 1; }
				else if (!northWall && southWall && !eastWall && !westWall) { value = "S   "; wallNumber = 1; }
				else if (!northWall && !southWall && eastWall && !westWall) { value = "E   "; wallNumber = 1; }
				else if (!northWall && !southWall && !eastWall && westWall) { value = "W   "; wallNumber = 1; }
				
				else if (!northWall && !southWall && !eastWall && !westWall) { value = "    "; wallNumber = 0; }
		}
		void setWestWall(boolean state) {
				this.westWall = state;
				if (northWall && southWall && eastWall && westWall) { value = "A   "; wallNumber = 4; }
				
				else if (!northWall && southWall && eastWall && westWall) { value = "SEW "; }
				else if (northWall && !southWall && eastWall && westWall) { value = "NEW "; }
				else if (northWall && southWall && !eastWall && westWall) { value = "NSW "; }
				else if (northWall && southWall && eastWall && !westWall) { value = "NSE "; }

				else if (!northWall && !southWall && eastWall && westWall) { value = "WE  "; wallNumber = 2; }
				else if (!northWall && southWall && !eastWall && westWall) { value = "SW  "; wallNumber = 2; }
				else if (!northWall && southWall && eastWall && !westWall) { value = "SE  "; wallNumber = 2; }
				
				else if (northWall && !southWall && !eastWall && westWall) { value = "NW  "; wallNumber = 2; }
				else if (northWall && !southWall && eastWall && !westWall) { value = "NE  "; wallNumber = 2; }
				
				else if (northWall && southWall && !eastWall && !westWall) { value = "NS  "; wallNumber = 2; }
				
				else if (northWall && !southWall && !eastWall && !westWall) { value = "N   "; wallNumber = 1; }
				else if (!northWall && southWall && !eastWall && !westWall) { value = "S   "; wallNumber = 1; }
				else if (!northWall && !southWall && eastWall && !westWall) { value = "E   "; wallNumber = 1; }
				else if (!northWall && !southWall && !eastWall && westWall) { value = "W   "; wallNumber = 1; }
				
				else if (!northWall && !southWall && !eastWall && !westWall) { value = "    "; wallNumber = 0; }
		}
		public String toString() {
				return value;
		}
}
class maze {
		box start;
		box end;
		int size;
		int[] originCoords = new int[2];
		box startBox;
		int deadEnds;
		static boolean in(ArrayList<int[]> arr1, int[] arr2) {
				for (int[] i : arr1) {
						if (i[0]==arr2[0] && i[1]==arr2[1]) {
								return true;
						}
				}
				return false;
		}
		static ArrayList<int[]> removeDuplicates(ArrayList<int[]> list) {
				ArrayList<int[]> newList = new ArrayList<int[]>();
				for (int i=0; i<list.size(); i++) {
						if (!newList.contains(list.get(i))) {
								newList.add(list.get(i));
						}
				}
				return newList;
		}
		public maze(int size, int deadEnds) {
				Random r = new Random();
				this.size = size;
				this.deadEnds = deadEnds;
				box north; box south; box east; box west;
				//Create grid
				for (int i=0; i<size; i++) {
						addBoxToColumn();
						for (int e=1; e<size; e++) {
								addBoxToRow();
						}
				}
				box wallCreator = start;
				for (int i=0; i<size; i++) {
						wallCreator = findRowStart(i);
						wallCreator.setNorthWall(true);
						wallCreator.setSouthWall(true);
						wallCreator.setEastWall(true);
						wallCreator.setWestWall(true);
						for (int e=1; e<size; e++) {
								wallCreator = wallCreator.east;
								wallCreator.setNorthWall(true);
								wallCreator.setSouthWall(true);
								wallCreator.setEastWall(true);
								wallCreator.setWestWall(true);
						}
				}
				box placeholder = start;
				int[][] winCoords = {{size/2, size/2}, {size/2-1, size/2-1}, {size/2-1, size/2}, {size/2, size/2-1}};
				int[] winCoord = new int[2];
				int[] solutionCoord = new int[2];
				boolean foundMiddle = false;
				box middleFix = start;
				while (!foundMiddle) {
						if (middleFix.x==winCoords[1][1] && middleFix.y==winCoords[1][0]) {
								foundMiddle = true;
								break;
						}
						if (middleFix.x==size-1) {
								middleFix = findRowStart(middleFix.y+1);
						}
						else {
								middleFix = middleFix.east;
						}
				}
				switch (r.nextInt(4)) {
						case 0:
								this.originCoords[0] = 0;
								this.originCoords[1] = 0;
								break;
						case 1:
								this.originCoords[0] = 0;
								this.originCoords[1] = size-1;
								break;
						case 2:
								this.originCoords[0] = size-1;
								this.originCoords[1] = 0;
								break;
						default:
								this.originCoords[0] = size-1;
								this.originCoords[1] = size-1;
								break;
				}
				box origin = start;
				outerloop:
				for (int i=0; i<size; i++) {
						origin = findRowStart(i);
						for (int e=0; e<size; e++) {
								if (origin.x==originCoords[1] && origin.y==originCoords[0]) {
										switch (r.nextInt(2)) {
												case 0:
														if (origin.x==0) { origin.setWestWall(false); }
														else { origin.setEastWall(false); }
														break;
												case 1:
														if (origin.y==0) { origin.setSouthWall(false); }
														else { origin.setNorthWall(false); }
														break;
										}
										break outerloop;
								}
								origin = origin.east;
						}
				}
				this.startBox = origin;
				foundMiddle = false;
				System.out.println("Coords to win: "+winCoord[0]+", "+winCoord[1]);
				System.out.println("Starting coord: "+originCoords[0]+", "+originCoords[1]);
				box wallMouse = origin;
				int duration;
				for (int i=0; i<deadEnds; i++) {
						switch (r.nextInt(4)) {
								case 0:
										//North
										if (wallMouse.y==0) {
												break;
										}
										else {
												if (wallMouse.northWall && wallMouse.x==0) {
														wallMouse.setEastWall(false);
														wallMouse = wallMouse.east;
														wallMouse.setWestWall(false);
												}
												else if (wallMouse.northWall && wallMouse.x==size-1) {
														wallMouse.setWestWall(false);
														wallMouse = wallMouse.west;
														wallMouse.setEastWall(false);
												}
												duration = r.nextInt(size-1);
												for (int e=0; e<duration; e++) {
														if (wallMouse.north.y==0) { break; }
														wallMouse.setNorthWall(false);
														wallMouse = wallMouse.north;
														wallMouse.setSouthWall(false);
												}
										}
										break;
								case 1:
										//South
										if (wallMouse.y==size-1) {
												break;
										}
										else {
												if (wallMouse.southWall && wallMouse.x==0) {
														wallMouse.setEastWall(false);
														wallMouse = wallMouse.east;
														wallMouse.setWestWall(false);
												}
												else if (wallMouse.southWall && wallMouse.x==size-1) {
														wallMouse.setWestWall(false);
														wallMouse = wallMouse.west;
														wallMouse.setEastWall(false);
												}
												duration = r.nextInt(size-1);
												for (int e=0; e<duration; e++) {
														if (wallMouse.south.y==size-1) { break; }
														wallMouse.setSouthWall(false);
														wallMouse = wallMouse.south;
														wallMouse.setNorthWall(false);
												}
										}
										break;
								case 2:
										//East
										if (wallMouse.x==size-1) {
												break;
										}
										else {
												if (wallMouse.eastWall && wallMouse.y==0) {
														wallMouse.setSouthWall(false);
														wallMouse = wallMouse.south;
														wallMouse.setNorthWall(false);
												}
												else if (wallMouse.eastWall && wallMouse.y==size-1) {
														wallMouse.setNorthWall(false);
														wallMouse = wallMouse.north;
														wallMouse.setSouthWall(false);
												}
												duration = r.nextInt(size-1);
												for (int e=0; e<duration; e++) {
														if (wallMouse.east.x==size-1) { break; }
														wallMouse.setEastWall(false);
														wallMouse = wallMouse.east;
														wallMouse.setWestWall(false);
												}
										}
										break;
								case 3:
										//West
										if (wallMouse.x==0) {
												break;
										}
										else {
												if (wallMouse.westWall && wallMouse.y==0) {
														wallMouse.setSouthWall(false);
														wallMouse = wallMouse.south;
														wallMouse.setNorthWall(false);
												}
												else if (wallMouse.westWall && wallMouse.y==size-1) {
														wallMouse.setNorthWall(false);
														wallMouse = wallMouse.north;
														wallMouse.setSouthWall(false);
												}
												duration = r.nextInt(size-1);
												for (int e=0; e<duration; e++) {
														if (wallMouse.west.x==0) { break; }
														wallMouse.setWestWall(false);
														wallMouse = wallMouse.west;
														wallMouse.setEastWall(false);
												}
										}
										break;
						}
				}
				box pathMouse = start;
				int openWall = r.nextInt(8);
				switch (openWall) {
						case 0:
								//Main wall
								middleFix.setNorthWall(false);
								middleFix.setWestWall(true);
								middleFix.setEastWall(false);
								middleFix.setSouthWall(false);
								//
								middleFix.east.setNorthWall(true);
								middleFix.east.setWestWall(false);
								middleFix.east.setEastWall(true);
								middleFix.east.setSouthWall(false);
								//
								middleFix.south.setNorthWall(false);
								middleFix.south.setWestWall(true);
								middleFix.south.setEastWall(false);
								middleFix.south.setSouthWall(true);
								//
								middleFix.south.east.setNorthWall(false);
								middleFix.south.east.setWestWall(false);
								middleFix.south.east.setEastWall(true);
								middleFix.south.east.setSouthWall(true);
								winCoord[0]=middleFix.y-1;
								winCoord[1]=middleFix.x;
								solutionCoord[0] = middleFix.y;
								solutionCoord[1] = middleFix.x;
								pathMouse = middleFix.north;
								pathMouse.setSouthWall(false);
								break;
						case 1:
								middleFix.setNorthWall(true);
								middleFix.setWestWall(false);
								middleFix.setEastWall(false);
								middleFix.setSouthWall(false);
								//
								middleFix.east.setNorthWall(true);
								middleFix.east.setWestWall(false);
								middleFix.east.setEastWall(true);
								middleFix.east.setSouthWall(false);
								//
								middleFix.south.setNorthWall(false);
								middleFix.south.setWestWall(true);
								middleFix.south.setEastWall(false);
								middleFix.south.setSouthWall(true);
								//
								middleFix.south.east.setNorthWall(false);
								middleFix.south.east.setWestWall(false);
								middleFix.south.east.setEastWall(true);
								middleFix.south.east.setSouthWall(true);
								winCoord[0]=middleFix.y;
								winCoord[1]=middleFix.x-1;
								solutionCoord[0] = middleFix.y;
								solutionCoord[1] = middleFix.x;
								pathMouse = middleFix.west;
								pathMouse.setEastWall(false);
								break;
						case 2:
								middleFix.east.setNorthWall(false);
								middleFix.east.setWestWall(false);
								middleFix.east.setEastWall(true);
								middleFix.east.setSouthWall(false);
								//
								middleFix.setNorthWall(true);
								middleFix.setWestWall(true);
								middleFix.setEastWall(false);
								middleFix.setSouthWall(false);
								//
								middleFix.south.setNorthWall(false);
								middleFix.south.setWestWall(true);
								middleFix.south.setEastWall(false);
								middleFix.south.setSouthWall(true);
								//
								middleFix.south.east.setNorthWall(false);
								middleFix.south.east.setWestWall(false);
								middleFix.south.east.setEastWall(true);
								middleFix.south.east.setSouthWall(true);
								winCoord[0]=middleFix.east.y-1;
								winCoord[1]=middleFix.east.x;
								solutionCoord[0] = middleFix.east.y;
								solutionCoord[1] = middleFix.east.x;
								pathMouse = middleFix.east.north;
								pathMouse.setSouthWall(false);
								break;
						case 3:
								middleFix.east.setNorthWall(true);
								middleFix.east.setWestWall(false);
								middleFix.east.setEastWall(false);
								middleFix.east.setSouthWall(false);
								//
								middleFix.setNorthWall(true);
								middleFix.setWestWall(true);
								middleFix.setEastWall(false);
								middleFix.setSouthWall(false);
								//
								middleFix.south.setNorthWall(false);
								middleFix.south.setWestWall(true);
								middleFix.south.setEastWall(false);
								middleFix.south.setSouthWall(true);
								//
								middleFix.south.east.setNorthWall(false);
								middleFix.south.east.setWestWall(false);
								middleFix.south.east.setEastWall(true);
								middleFix.south.east.setSouthWall(true);
								winCoord[0]=middleFix.east.y;
								winCoord[1]=middleFix.east.x+1;
								solutionCoord[0] = middleFix.east.y;
								solutionCoord[1] = middleFix.east.x;
								pathMouse = middleFix.east.east;
								pathMouse.setWestWall(false);
								break;
						case 4:
								middleFix.south.setNorthWall(false);
								middleFix.south.setWestWall(true);
								middleFix.south.setEastWall(false);
								middleFix.south.setSouthWall(false);
								//
								middleFix.setNorthWall(true);
								middleFix.setWestWall(true);
								middleFix.setEastWall(false);
								middleFix.setSouthWall(false);
								//
								middleFix.east.setNorthWall(true);
								middleFix.east.setWestWall(false);
								middleFix.east.setEastWall(true);
								middleFix.east.setSouthWall(false);
								//
								middleFix.south.east.setNorthWall(false);
								middleFix.south.east.setWestWall(false);
								middleFix.south.east.setEastWall(true);
								middleFix.south.east.setSouthWall(true);
								winCoord[0]=middleFix.south.y+1;
								winCoord[1]=middleFix.south.x;
								solutionCoord[0] = middleFix.south.y;
								solutionCoord[1] = middleFix.south.x;
								pathMouse = middleFix.south.south;
								pathMouse.setNorthWall(false);
								break;
						case 5:
								middleFix.south.setNorthWall(false);
								middleFix.south.setWestWall(false);
								middleFix.south.setEastWall(false);
								middleFix.south.setSouthWall(true);
								//
								middleFix.setNorthWall(true);
								middleFix.setWestWall(true);
								middleFix.setEastWall(false);
								middleFix.setSouthWall(false);
								//
								middleFix.east.setNorthWall(true);
								middleFix.east.setWestWall(false);
								middleFix.east.setEastWall(true);
								middleFix.east.setSouthWall(false);
								//
								middleFix.south.east.setNorthWall(false);
								middleFix.south.east.setWestWall(false);
								middleFix.south.east.setEastWall(true);
								middleFix.south.east.setSouthWall(true);
								winCoord[0]=middleFix.south.y;
								winCoord[1]=middleFix.south.x-1;
								solutionCoord[0] = middleFix.south.y;
								solutionCoord[1] = middleFix.south.x;
								pathMouse = middleFix.south.west;
								pathMouse.setEastWall(false);
								break;
						case 6:
								middleFix.south.east.setNorthWall(false);
								middleFix.south.east.setWestWall(false);
								middleFix.south.east.setEastWall(true);
								middleFix.south.east.setSouthWall(false);
								//
								middleFix.setNorthWall(true);
								middleFix.setWestWall(true);
								middleFix.setEastWall(false);
								middleFix.setSouthWall(false);
								//
								middleFix.east.setNorthWall(true);
								middleFix.east.setWestWall(false);
								middleFix.east.setEastWall(true);
								middleFix.east.setSouthWall(false);
								//
								middleFix.south.setNorthWall(false);
								middleFix.south.setWestWall(true);
								middleFix.south.setEastWall(false);
								middleFix.south.setSouthWall(true);
								winCoord[0]=middleFix.south.east.y+1;
								winCoord[1]=middleFix.south.east.x;
								solutionCoord[0] = middleFix.south.east.y;
								solutionCoord[1] = middleFix.south.east.x;
								pathMouse = middleFix.south.east.south;
								pathMouse.setNorthWall(false);
								break;
						case 7:
								middleFix.south.east.setNorthWall(false);
								middleFix.south.east.setWestWall(false);
								middleFix.south.east.setEastWall(false);
								middleFix.south.east.setSouthWall(true);
								//
								middleFix.setNorthWall(true);
								middleFix.setWestWall(true);
								middleFix.setEastWall(false);
								middleFix.setSouthWall(false);
								//
								middleFix.east.setNorthWall(true);
								middleFix.east.setWestWall(false);
								middleFix.east.setEastWall(true);
								middleFix.east.setSouthWall(false);
								//
								middleFix.south.setNorthWall(false);
								middleFix.south.setWestWall(true);
								middleFix.south.setEastWall(false);
								middleFix.south.setSouthWall(true);
								winCoord[0]=middleFix.south.east.y;
								winCoord[1]=middleFix.south.east.x+1;
								solutionCoord[0] = middleFix.south.east.y;
								solutionCoord[1] = middleFix.south.east.x;
								pathMouse = middleFix.south.east.east;
								pathMouse.setWestWall(false);
								break;
				}
				boolean foundPath = false;
				int previousDirection = -1;
				//Fix this
				while (!foundPath) {
						if (pathMouse.north!=null && pathMouse.north.y!=size/2 && pathMouse.north.wallNumber<3 && !pathMouse.northWall) {
								System.out.println("Condition 1");
								foundPath = true; break;
						}
						if (pathMouse.east!=null && pathMouse.east.x!=size/2-1 && pathMouse.east.wallNumber<3 && !pathMouse.eastWall) {
								System.out.println("Condition 2");
								foundPath = true; break;
						}
						if (pathMouse.south!=null && pathMouse.south.y!=size/2-1 && pathMouse.south.wallNumber<3 && !pathMouse.southWall) {
								System.out.println("Condition 3");
								foundPath = true; break;
						}
						if (pathMouse.west!=null && pathMouse.west.x!=size/2 && pathMouse.west.wallNumber<3 && !pathMouse.westWall) {
								System.out.println("Condition 4");
								foundPath = true; break;
						}
						switch (r.nextInt(4)) {
								case 0:
										//North
										if (pathMouse.y==0 || pathMouse.north.y==size/2 || previousDirection==0) {
												break;
										}
										else {
												duration = r.nextInt(size-1);
												for (int e=0; e<duration; e++) {
														if (pathMouse.north==null || pathMouse.north.y==0 || pathMouse.north.y==size/2) { break; }
														pathMouse.setNorthWall(false);
														pathMouse = pathMouse.north;
														System.out.println("Moved north");
														previousDirection = 0;
														pathMouse.setSouthWall(false);
												}
										}
										break;
								case 1:
										//South
										if (pathMouse.y==size-1 || pathMouse.south.y==size/2-1 || previousDirection==2) {
												break;
										}
										else {
												duration = r.nextInt(size-1);
												for (int e=0; e<duration; e++) {
														if (pathMouse.south==null || pathMouse.south.y==size-1 || pathMouse.south.y==size/2-1) { break; }
														pathMouse.setSouthWall(false);
														pathMouse = pathMouse.south;
														System.out.println("Moved south");
														previousDirection = 2;
														pathMouse.setNorthWall(false);
												}
										}
										break;
								case 2:
										//East
										if (pathMouse.x==size-1 || pathMouse.east.x==size/2-1 || previousDirection==1) {
												break;
										}
										else {
												duration = r.nextInt(size-1);
												for (int e=0; e<duration; e++) {
														if (pathMouse.east==null || pathMouse.east.x==size-1 || pathMouse.east.x==size/2-1) { break; }
														pathMouse.setEastWall(false);
														pathMouse = pathMouse.east;
														System.out.println("Moved east");
														previousDirection = 1;
														pathMouse.setWestWall(false);
												}
										}
										break;
								case 3:
										//West
										if (pathMouse.x==0 || pathMouse.west.x==size/2 || previousDirection==3) {
												break;
										}
										else {
												duration = r.nextInt(size-1);
												for (int e=0; e<duration; e++) {
														if (pathMouse.west==null || pathMouse.west.x==0 || pathMouse.west.x==size/2) { break; }
														pathMouse.setWestWall(false);
														pathMouse = pathMouse.west;
														System.out.println("Moved west");
														previousDirection = 3;
														pathMouse.setEastWall(false);
												}
										}
										break;
						}
				}
				if (origin.x==0) {
						origin.setWestWall(true);
				}
				else {
						origin.setEastWall(true);
				}
				if (origin.y==0) {
						origin.setNorthWall(true);
				}
				else {
						origin.setSouthWall(true);
				}
		}
		public String toString() {
				String result = new String();
				box placeholder = start;
				for (int i=0; i<size; i++) {
						placeholder = findRowStart(i);
						for (int e=0; e<size; e++) {
								result+=placeholder.toString();
								placeholder = placeholder.east;
						}
						result+="\n";
				}
				return result;
		}
		box findRowStart(int column) {
				box selectedBox = start;
				while (selectedBox.y!=column) {
						selectedBox = selectedBox.south;
				}
				return selectedBox;
		}
		void addBoxToRow() {
				final box l = end;
				final box above;
				if (l!=null && l.north!=null && l.north.east!=null) {
						above = l.north.east;
				}
				else {
						above = null;
				}
				box newBox = new box(above, null, null, l);
				end = newBox;
				if (start==null) {
						start = newBox;
				}
				else {
						l.east = newBox;
						l.setEastWall(false);// = false;
						if (above!=null) {
								above.south = newBox;
								above.setSouthWall(false);// = false;
						}
				}
		}
		void addBoxToColumn() {
				final box l = end;
				final box above;
				if (l!=null) {
						above = findRowStart(l.y);
				}
				else {
						above = null;
				}
				box newBox = new box(above, null, null, null);
				end = newBox;
				if (start==null) {
						start = newBox;
				}
				else {
						above.south = newBox;
						above.setSouthWall(false);
				}
		}
}
class micromouse {
		maze m;
		int[] startCoords;
		box position;
		Integer orientation;
		int duration = 0;
		public micromouse(maze m) {
				this.m = m;
				this.startCoords = m.originCoords;
				this.position = m.startBox;
		}
		Boolean[] checkWalls() {
				Boolean[] walls = new Boolean[4];
				if (position.northWall) { walls[0]=true; }
				else { walls[0]=false; }
				if (position.eastWall) { walls[1]=true; }
				else { walls[1]=false; }
				if (position.southWall) { walls[2]=true; }
				else { walls[2]=false; }
				if (position.westWall) { walls[3]=true; }
				else { walls[3]=false; }
				return walls;
		}
		Boolean[] checkLongWalls() {
				Boolean[] walls = new Boolean[4];
				if (position.north!=null) {
						if (position.north.northWall) { walls[0]=true; }
						else { walls[0]=false; }
				}
				else { walls[0] = true; }
				if (position.east!=null) {
						if (position.east.eastWall) { walls[1]=true; }
						else { walls[1]=false; }
				}
				else { walls[1] = true; }
				if (position.south!=null) {
						if (position.south.southWall) { walls[2]=true; }
						else { walls[2]=false; }
				}
				else { walls[2] = true; }
				if (position.west!=null) {
						if (position.west.westWall) { walls[3]=true; }
						else { walls[3]=false; }
				}
				else { walls[3] = true; }
				return walls;
		}
		void setOrientation(int orientation) { this.orientation = orientation; }
		boolean moveNorth() {
				if (!position.northWall && !position.north.southWall) { position = position.north; duration++; return true; }
				else { return false; }
		}
		boolean moveSouth() {
				if (!position.southWall && !position.south.northWall) { position = position.south; duration++; return true; }
				else { return false; }
		}
		boolean moveEast() {
				if (!position.eastWall && !position.east.westWall) { position = position.east; duration++; return true; }
				else { return false; }
		}
		boolean moveWest() {
				if (!position.westWall && !position.west.eastWall) { position = position.west; duration++; return true; }
				else { return false; }
		}
}
public class microMouseSimulation {
		static int getWallIndex(Boolean[] walls) {
				if (walls[0] && walls[2] && walls[1] && walls[3]) { return 14; }
				
				else if (!walls[0] && walls[2] && walls[1] && walls[3]) { return 10; }
				else if (walls[0] && !walls[2] && walls[1] && walls[3]) { return 12; }
				else if (walls[0] && walls[2] && !walls[1] && walls[3]) { return 11; }
				else if (walls[0] && walls[2] && walls[1] && !walls[3]) { return 13; }

				else if (!walls[0] && !walls[2] && walls[1] && walls[3]) { return 9; }
				else if (!walls[0] && walls[2] && !walls[1] && walls[3]) { return 8; }
				else if (!walls[0] && walls[2] && walls[1] && !walls[3]) { return 7; }
				
				else if (walls[0] && !walls[2] && !walls[1] && walls[3]) { return 6; }
				else if (walls[0] && !walls[2] && walls[1] && !walls[3]) { return 4; }
				
				else if (walls[0] && walls[2] && !walls[1] && !walls[3]) { return 5; }
				
				else if (walls[0] && !walls[2] && !walls[1] && !walls[3]) { return 0; }
				else if (!walls[0] && walls[2] && !walls[1] && !walls[3]) { return 2; }
				else if (!walls[0] && !walls[2] && walls[1] && !walls[3]) { return 1; }
				else if (!walls[0] && !walls[2] && !walls[1] && walls[3]) { return 3; }
				
				else if (!walls[0] && !walls[2] && !walls[1] && !walls[3]) { return 15; }
				
				else { return -1; }
		}
		static int[] findLocation(int[][] array, int value) {
				int[] results = {-1, -1};
				for (int i=0; i<array.length; i++) {
						for (int e=0; e<array[0].length; e++) {
								if (array[i][e]==value) {
										results[0]=i; results[1]=e;
										break;
								}
						}
				}
				return results;
		}
		static void displayConstruct(int[][] maze) {
				for (int i=0; i<maze.length; i++) {
						for (int e=0; e<maze[0].length; e++) {
								if (maze[i][e]<10) {
										System.out.print(maze[i][e]+"  ");
								}
								else if (maze[i][e]<100) {
										System.out.print(maze[i][e]+" ");
								}
								else {
										System.out.print(maze[i][e]);
								}
						}
						System.out.println();
				}
		}
		public static void main(String[] args) {
				Scanner s = new Scanner(System.in);
				Scanner sI = new Scanner(System.in);
				Random dir = new Random();
				System.out.print("Enter in the size of the maze (it will be a square): ");
				int mazeSize = sI.nextInt();
				System.out.print("Enter in the randomness factor of the maze: ");
				int randomnessFactor = sI.nextInt();
				maze m = new maze(mazeSize, randomnessFactor);
				System.out.print(m.toString());
				s.nextLine();
				micromouse mouse = new micromouse(m);
				boolean foundMiddle = false;
				//Gets mouse orientation
				Boolean[] walls = mouse.checkWalls();
				Boolean[] farWalls = new Boolean[4];
				if (!walls[0]) { mouse.setOrientation(0); }
				else if (!walls[1]) { mouse.setOrientation(1); }
				else if (!walls[2]) { mouse.setOrientation(2); }
				else if (!walls[3]) { mouse.setOrientation(3); }
				//North, West
				int[][] mathmaticalMaze1 = new int[mazeSize][mazeSize];
				//South, East
				int[][] mathmaticalMaze2 = new int[mazeSize][mazeSize];
				int[][] masterMaze = new int[mazeSize][mazeSize];
				masterMaze[mazeSize/2][mazeSize/2] = 69;
				masterMaze[mazeSize/2][mazeSize/2-1] = 69;
				masterMaze[mazeSize/2-1][mazeSize/2] = 69;
				masterMaze[mazeSize/2-1][mazeSize/2-1] = 69;
				for (int i=0; i<mathmaticalMaze1.length; i++) {
						for (int e=0; e<mathmaticalMaze1.length; e++) {
								mathmaticalMaze1[i][e] = 16;
								mathmaticalMaze2[i][e] = 16;
						}
				}
				int x=0, y=0;
				int wallIndex = -1;
				int delay = 1;
				boolean validMove = false;
				switch (mouse.orientation) {
						case 0:
								mathmaticalMaze1[mazeSize-1][0] = 18;
								mathmaticalMaze2[mazeSize-1][mazeSize-1] = 18;
								walls = mouse.checkWalls();
								while (!walls[0]) {
										validMove = mouse.moveNorth();
										if (!validMove) { break; }
										System.out.println("Moved North");
										y++;
										walls = mouse.checkWalls();
										wallIndex = getWallIndex(walls);
										if (walls[1] && walls[3] && (mathmaticalMaze1[mazeSize-y][0]==18 || mathmaticalMaze1[mazeSize-y][0]==17) && (mathmaticalMaze2[mazeSize-y][mazeSize-1]==18 || mathmaticalMaze2[mazeSize-y][mazeSize-1]==17)) {
												mathmaticalMaze1[mazeSize-1-y][0] = 17; //West
												mathmaticalMaze2[mazeSize-1-y][mazeSize-1] = 17; //East
										}
										else {
												mathmaticalMaze1[mazeSize-1-y][0] = wallIndex; //West
												mathmaticalMaze2[mazeSize-1-y][mazeSize-1] = wallIndex; //East
										}
										System.out.println("Option 1: ");
										displayConstruct(mathmaticalMaze1);
										System.out.println("Option 2: ");
										displayConstruct(mathmaticalMaze2);
								}
								if (!walls[1]) { masterMaze = mathmaticalMaze1; masterMaze[mazeSize-1-y][0] = 42; }
								else if (!walls[3]) { masterMaze = mathmaticalMaze2; masterMaze[mazeSize-1-y][mazeSize-1] = 42; }
								System.out.println("Maze waveform collapse: ");
								displayConstruct(masterMaze);
								break;
						case 1:
								mathmaticalMaze1[0][0] = 18;
								mathmaticalMaze2[mazeSize-1][0] = 18;
								walls = mouse.checkWalls();
								while (!walls[1]) {
										validMove = mouse.moveEast();
										if (!validMove) { break; }
										System.out.println("Moved East");
										x++;
										walls = mouse.checkWalls();
										wallIndex = getWallIndex(walls);
										if (walls[0] && walls[2] && (mathmaticalMaze1[0][x-1]==18 || mathmaticalMaze1[0][x-1]==17) && (mathmaticalMaze2[mazeSize-1][x-1]==18 || mathmaticalMaze2[mazeSize-1][x-1]==17)) {
												mathmaticalMaze1[0][x] = 17; //North
												mathmaticalMaze2[mazeSize-1][x] = 17; //South
										}
										else {
												mathmaticalMaze1[0][x] = wallIndex; //North
												mathmaticalMaze2[mazeSize-1][x] = wallIndex; //South
										}
										System.out.println("Option 1: ");
										displayConstruct(mathmaticalMaze1);
										System.out.println("Option 2: ");
										displayConstruct(mathmaticalMaze2);
								}
								if (!walls[0]) { masterMaze = mathmaticalMaze2; masterMaze[mazeSize-1][x] = 42; }
								else if (!walls[2]) { masterMaze = mathmaticalMaze1; masterMaze[0][x] = 42; }
								System.out.println("Maze waveform collapse: ");
								displayConstruct(masterMaze);
								break;
						case 2:
								mathmaticalMaze1[0][0] = 18;
								mathmaticalMaze2[0][mazeSize-1] = 18;
								walls = mouse.checkWalls();
								while (!mouse.checkWalls()[2]) {
										validMove = mouse.moveSouth();
										if (!validMove) { break; }
										System.out.println("Moved South");
										y++;
										walls = mouse.checkWalls();
										wallIndex = getWallIndex(walls);
										if (walls[1] && walls[3] && (mathmaticalMaze1[y-1][0]==18 || mathmaticalMaze1[y-1][0]==17) && (mathmaticalMaze2[y-1][mazeSize-1]==18 || mathmaticalMaze2[y-1][mazeSize-1]==17)) {
												mathmaticalMaze1[y][0] = 17; //West
												mathmaticalMaze2[y][mazeSize-1] = 17; //East
										}
										else {
												mathmaticalMaze1[y][0] = wallIndex; //West
												mathmaticalMaze2[y][mazeSize-1] = wallIndex; //East
										}
										System.out.println("Option 1: ");
										displayConstruct(mathmaticalMaze1);
										System.out.println("Option 2: ");
										displayConstruct(mathmaticalMaze2);
								}
								if (!walls[1]) { masterMaze = mathmaticalMaze1; masterMaze[y][0] = 42; }
								else if (!walls[3]) { masterMaze = mathmaticalMaze2; masterMaze[y][mazeSize-1] = 42; }
								System.out.println("Maze waveform collapse: ");
								displayConstruct(masterMaze);
								break;
						case 3:
								mathmaticalMaze1[0][mazeSize-1] = 18;
								mathmaticalMaze2[mazeSize-1][mazeSize-1] = 18;
								walls = mouse.checkWalls();
								while (!mouse.checkWalls()[3]) {
										validMove = mouse.moveWest();
										if (!validMove) { break; }
										System.out.println("Moved West");
										x++;
										walls = mouse.checkWalls();
										wallIndex = getWallIndex(walls);
										if (walls[0] && walls[2] && (mathmaticalMaze1[0][mazeSize-x]==18 || mathmaticalMaze1[0][mazeSize-x]==17) && (mathmaticalMaze2[mazeSize-1][mazeSize-x]==18 || mathmaticalMaze2[mazeSize-1][mazeSize-x]==17)) {
												mathmaticalMaze1[0][mazeSize-1-x] = 17;
												mathmaticalMaze2[mazeSize-1][mazeSize-1-x] = 17;
										}
										else {
												mathmaticalMaze1[0][mazeSize-1-x] = wallIndex;
												mathmaticalMaze2[mazeSize-1][mazeSize-1-x] = wallIndex;
										}
										System.out.println("Option 1: ");
										displayConstruct(mathmaticalMaze1);
										System.out.println("Option 2: ");
										displayConstruct(mathmaticalMaze2);
								}
								if (!walls[0]) { masterMaze = mathmaticalMaze2; masterMaze[mazeSize-1][mazeSize-1-x] = 42; }
								else if (!walls[2]) { masterMaze = mathmaticalMaze1; masterMaze[0][mazeSize-1-x] = 42; }
								System.out.println("Maze waveform collapse: ");
								displayConstruct(masterMaze);
								break;
				}
				while (!foundMiddle) {
						walls = mouse.checkWalls();
						farWalls = mouse.checkLongWalls();
						wallIndex = getWallIndex(walls);
						int[] location = findLocation(masterMaze, 42);
						//Main thing
						int wallNumber = 4;
						if (!walls[0] && masterMaze[location[0]-1][location[1]]!=17) { wallNumber--; }
						if (!walls[1] && masterMaze[location[0]][location[1]+1]!=17) { wallNumber--; }
						if (!walls[2] && masterMaze[location[0]+1][location[1]]!=17) { wallNumber--; }
						if (!walls[3] && masterMaze[location[0]][location[1]-1]!=17) { wallNumber--; }
						//Two options
						if (wallNumber<3) {
								System.out.println("If: 0");
								switch (dir.nextInt(2)) {
										case 0:
												//North, east
												if (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
														System.out.println("If: 1");
														//Move north until wall
														while (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
																if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																		foundMiddle = true;
																		break;
																}
																if ((walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																		masterMaze[location[0]][location[1]] = 17;
																}
																else {
																		masterMaze[location[0]][location[1]] = wallIndex;
																}
																validMove = mouse.moveNorth();
																if (!validMove) { break; }
																System.out.println("Moved North: 4");
																location[0]--;
																masterMaze[location[0]][location[1]] = 42;
																displayConstruct(masterMaze);
																walls = mouse.checkWalls();
																wallIndex = getWallIndex(walls);
																if ((!walls[1] && masterMaze[location[0]][location[1]]!=17 && masterMaze[location[0]][location[1]]!=18) || (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18) && masterMaze[location[0]-1][location[1]]!=16) {
																		System.out.println("If: 2");
																		if (!walls[1] && !walls[3]) {
																				switch (dir.nextInt(2)) {
																						case 0:
																								if (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
																										if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																												foundMiddle = true;
																												break;
																										}
																										if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																												masterMaze[location[0]][location[1]] = 17;
																										}
																										else {
																												masterMaze[location[0]][location[1]] = wallIndex;
																										}
																										validMove = mouse.moveEast();
																										if (!validMove) { break; }
																										System.out.println("Moved East: 0");
																										location[1]++;
																										masterMaze[location[0]][location[1]] = 42;
																										displayConstruct(masterMaze);
																										walls = mouse.checkWalls();
																										wallIndex = getWallIndex(walls);
																										try { TimeUnit.MILLISECONDS.sleep(delay); }
																										catch (Exception InterruptedException) {}
																								}
																								masterMaze[location[0]][location[1]] = 42;
																								break;
																						case 1:
																								if (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18) {
																										if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																												foundMiddle = true;
																												break;
																										}
																										if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17)) {
																												masterMaze[location[0]][location[1]] = 17;
																										}
																										else {
																												masterMaze[location[0]][location[1]] = wallIndex;
																										}
																										validMove = mouse.moveWest();
																										if (!validMove) { break; }
																										System.out.println("Moved West: 1");
																										location[1]--;
																										masterMaze[location[0]][location[1]] = 42;
																										displayConstruct(masterMaze);
																										walls = mouse.checkWalls();
																										wallIndex = getWallIndex(walls);
																										try { TimeUnit.MILLISECONDS.sleep(delay); }
																										catch (Exception InterruptedException) {}
																								}
																								masterMaze[location[0]][location[1]] = 42;
																								break;
																				}
																		}
																		else if (!walls[1]) {
																				if (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveEast();
																						if (!validMove) { break; }
																						System.out.println("Moved East: 2");
																						location[1]++;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																		}
																		else {
																				if (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveWest();
																						if (!validMove) { break; }
																						System.out.println("Moved West: 3");
																						location[1]--;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																		}
																		break;
																}
																try { TimeUnit.MILLISECONDS.sleep(delay); }
																catch (Exception InterruptedException) {}
														}
														masterMaze[location[0]][location[1]] = 42;
												}
												else if (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
														System.out.println("If: 3");
														//move east until wall
														while (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
																if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																		foundMiddle = true;
																		break;
																}
																if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																		masterMaze[location[0]][location[1]] = 17;
																}
																else {
																		masterMaze[location[0]][location[1]] = wallIndex;
																}
																validMove = mouse.moveEast();
																if (!validMove) { break; }
																System.out.println("Moved East: 9");
																location[1]++;
																masterMaze[location[0]][location[1]] = 42;
																displayConstruct(masterMaze);
																walls = mouse.checkWalls();
																wallIndex = getWallIndex(walls);
																if (((!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) || (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18)) && masterMaze[location[0]][location[1]+1]!=16) {
																		System.out.println("If: 4");
																		if (!walls[0] && !walls[2]) {
																				switch (dir.nextInt(2)) {
																						case 0:
																								if (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
																										if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																												foundMiddle = true;
																												break;
																										}
																										if ((walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																												masterMaze[location[0]][location[1]] = 17;
																										}
																										else {
																												masterMaze[location[0]][location[1]] = wallIndex;
																										}
																										validMove = mouse.moveNorth();
																										if (!validMove) { break; }
																										System.out.println("Moved North: 5");
																										location[0]--;
																										masterMaze[location[0]][location[1]] = 42;
																										displayConstruct(masterMaze);
																										walls = mouse.checkWalls();
																										wallIndex = getWallIndex(walls);
																										try { TimeUnit.MILLISECONDS.sleep(delay); }
																										catch (Exception InterruptedException) {}
																								}
																								masterMaze[location[0]][location[1]] = 42;
																								break;
																						case 1:
																								if (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
																										if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																												foundMiddle = true;
																												break;
																										}
																										if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																												masterMaze[location[0]][location[1]] = 17;
																										}
																										else {
																												masterMaze[location[0]][location[1]] = wallIndex;
																										}
																										validMove = mouse.moveSouth();
																										if (!validMove) { break; }
																										System.out.println("Moved South: 6");
																										location[0]++;
																										masterMaze[location[0]][location[1]] = 42;
																										displayConstruct(masterMaze);
																										walls = mouse.checkWalls();
																										wallIndex = getWallIndex(walls);
																										try { TimeUnit.MILLISECONDS.sleep(delay); }
																										catch (Exception InterruptedException) {}
																								}
																								masterMaze[location[0]][location[1]] = 42;
																								break;
																				}
																		}
																		else if (!walls[0]) {
																				if (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveNorth();
																						if (!validMove) { break; }
																						System.out.println("Moved North: 7");
																						location[0]--;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																		}
																		else {
																				if (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveSouth();
																						if (!validMove) { break; }
																						System.out.println("Moved South: 8");
																						location[0]++;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																		}
																		break;
																}
																try { TimeUnit.MILLISECONDS.sleep(delay); }
																catch (Exception InterruptedException) {}
														}
														masterMaze[location[0]][location[1]] = 42;
												}
												break;
										case 1:
												//South, west
												if (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
														System.out.println("If: 5");
														//move south until wall
														while (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
																if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																		foundMiddle = true;
																		break;
																}
																if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																		masterMaze[location[0]][location[1]] = 17;
																}
																else {
																		masterMaze[location[0]][location[1]] = wallIndex;
																}
																validMove = mouse.moveSouth();
																if (!validMove) { break; }
																System.out.println("Moved South: 14");
																location[0]++;
																masterMaze[location[0]][location[1]] = 42;
																displayConstruct(masterMaze);
																walls = mouse.checkWalls();
																wallIndex = getWallIndex(walls);
																if (((!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) || (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18)) && masterMaze[location[0]+1][location[1]]!=16) {
																		System.out.println("If: 6");
																		if (!walls[1] && !walls[3]) {
																				switch (dir.nextInt(2)) {
																						case 0:
																								if (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
																										if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																												foundMiddle = true;
																												break;
																										}
																										if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																												masterMaze[location[0]][location[1]] = 17;
																										}
																										else {
																												masterMaze[location[0]][location[1]] = wallIndex;
																										}
																										validMove = mouse.moveEast();
																										if (!validMove) { break; }
																										System.out.println("Moved East: 10");
																										location[1]++;
																										masterMaze[location[0]][location[1]] = 42;
																										displayConstruct(masterMaze);
																										walls = mouse.checkWalls();
																										wallIndex = getWallIndex(walls);
																										try { TimeUnit.MILLISECONDS.sleep(delay); }
																										catch (Exception InterruptedException) {}
																								}
																								masterMaze[location[0]][location[1]] = 42;
																								break;
																						case 1:
																								if (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18) {
																										if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																												foundMiddle = true;
																												break;
																										}
																										if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17)) {
																												masterMaze[location[0]][location[1]] = 17;
																										}
																										else {
																												masterMaze[location[0]][location[1]] = wallIndex;
																										}
																										validMove = mouse.moveWest();
																										if (!validMove) { break; }
																										System.out.println("Moved West: 11");
																										location[1]--;
																										masterMaze[location[0]][location[1]] = 42;
																										displayConstruct(masterMaze);
																										walls = mouse.checkWalls();
																										wallIndex = getWallIndex(walls);
																										try { TimeUnit.MILLISECONDS.sleep(delay); }
																										catch (Exception InterruptedException) {}
																								}
																								masterMaze[location[0]][location[1]] = 42;
																								break;
																				}
																		}
																		else if (!walls[1]) {
																				if (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveEast();
																						if (!validMove) { break; }
																						System.out.println("Moved East: 12");
																						location[1]++;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																		}
																		else {
																				if (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveWest();
																						if (!validMove) { break; }
																						System.out.println("Moved West: 13");
																						location[1]--;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																		}
																		break;
																}
																try { TimeUnit.MILLISECONDS.sleep(delay); }
																catch (Exception InterruptedException) {}
														}
														masterMaze[location[0]][location[1]] = 42;
												}
												else if (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18) {
														System.out.println("If: 7");
														//move west until wall
														while (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18) {
																if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																		foundMiddle = true;
																		break;
																}
																if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17)) {
																		masterMaze[location[0]][location[1]] = 17;
																}
																else {
																		masterMaze[location[0]][location[1]] = wallIndex;
																}
																validMove = mouse.moveWest();
																if (!validMove) { break; }
																System.out.println("Moved West: 19");
																location[1]--;
																masterMaze[location[0]][location[1]] = 42;
																displayConstruct(masterMaze);
																walls = mouse.checkWalls();
																wallIndex = getWallIndex(walls);
																if (((!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) || (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18)) && masterMaze[location[0]][location[1]-1]!=16) {
																		System.out.println("If: 8");
																		if (!walls[0] && !walls[2]) {
																				switch (dir.nextInt(2)) {
																						case 0:
																								if (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
																										if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																												foundMiddle = true;
																												break;
																										}
																										if ((walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																												masterMaze[location[0]][location[1]] = 17;
																										}
																										else {
																												masterMaze[location[0]][location[1]] = wallIndex;
																										}
																										validMove = mouse.moveNorth();
																										if (!validMove) { break; }
																										System.out.println("Moved North: 15");
																										location[0]--;
																										masterMaze[location[0]][location[1]] = 42;
																										displayConstruct(masterMaze);
																										walls = mouse.checkWalls();
																										wallIndex = getWallIndex(walls);
																										try { TimeUnit.MILLISECONDS.sleep(delay); }
																										catch (Exception InterruptedException) {}
																								}
																								masterMaze[location[0]][location[1]] = 42;
																								break;
																						case 1:
																								if (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
																										if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																												foundMiddle = true;
																												break;
																										}
																										if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																												masterMaze[location[0]][location[1]] = 17;
																										}
																										else {
																												masterMaze[location[0]][location[1]] = wallIndex;
																										}
																										validMove = mouse.moveSouth();
																										if (!validMove) { break; }
																										System.out.println("Moved South: 16");
																										location[0]++;
																										masterMaze[location[0]][location[1]] = 42;
																										displayConstruct(masterMaze);
																										walls = mouse.checkWalls();
																										wallIndex = getWallIndex(walls);
																										try { TimeUnit.MILLISECONDS.sleep(delay); }
																										catch (Exception InterruptedException) {}
																								}
																								masterMaze[location[0]][location[1]] = 42;
																								break;
																				}
																		}
																		else if (!walls[0]) {
																				if (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveNorth();
																						if (!validMove) { break; }
																						System.out.println("Moved North: 17");
																						location[0]--;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																		}
																		else {
																				if (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveSouth();
																						if (!validMove) { break; }
																						System.out.println("Moved South: 18");
																						location[0]++;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																		}
																		break;
																}
																try { TimeUnit.MILLISECONDS.sleep(delay); }
																catch (Exception InterruptedException) {}
														}
														masterMaze[location[0]][location[1]] = 42;
												}
												break;
								}
						}
						else {
								System.out.println("If: 9");
								//fix for dead ends
								if (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
										System.out.println("If: 10");
										//Move north until wall
										while (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
												if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
														foundMiddle = true;
														break;
												}
												if ((walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
														masterMaze[location[0]][location[1]] = 17;
												}
												else {
														masterMaze[location[0]][location[1]] = wallIndex;
												}
												validMove = mouse.moveNorth();
												if (!validMove) { break; }
												System.out.println("Moved North: 24");
												location[0]--;
												masterMaze[location[0]][location[1]] = 42;
												displayConstruct(masterMaze);
												walls = mouse.checkWalls();
												wallIndex = getWallIndex(walls);
												if (((!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) || (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18)) && masterMaze[location[0]-1][location[1]]!=16) {
														System.out.println("If: 11");
														if (!walls[1] && !walls[3]) {
																switch (dir.nextInt(2)) {
																		case 0:
																				if (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveEast();
																						if (!validMove) { break; }
																						System.out.println("Moved East: 20");
																						location[1]++;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																				break;
																		case 1:
																				if (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveWest();
																						if (!validMove) { break; }
																						System.out.println("Moved West: 21");
																						location[1]--;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																				break;
																}
														}
														else if (!walls[1]) {
																if (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
																		if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																				foundMiddle = true;
																				break;
																		}
																		if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																				masterMaze[location[0]][location[1]] = 17;
																		}
																		else {
																				masterMaze[location[0]][location[1]] = wallIndex;
																		}
																		validMove = mouse.moveEast();
																		if (!validMove) { break; }
																		System.out.println("Moved East: 22");
																		location[1]++;
																		masterMaze[location[0]][location[1]] = 42;
																		displayConstruct(masterMaze);
																		walls = mouse.checkWalls();
																		wallIndex = getWallIndex(walls);
																		try { TimeUnit.MILLISECONDS.sleep(delay); }
																		catch (Exception InterruptedException) {}
																}
																masterMaze[location[0]][location[1]] = 42;
														}
														else {
																if (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18) {
																		if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																				foundMiddle = true;
																				break;
																		}
																		if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17)) {
																				masterMaze[location[0]][location[1]] = 17;
																		}
																		else {
																				masterMaze[location[0]][location[1]] = wallIndex;
																		}
																		validMove = mouse.moveWest();
																		if (!validMove) { break; }
																		System.out.println("Moved West: 23");
																		location[1]--;
																		masterMaze[location[0]][location[1]] = 42;
																		displayConstruct(masterMaze);
																		walls = mouse.checkWalls();
																		wallIndex = getWallIndex(walls);
																		try { TimeUnit.MILLISECONDS.sleep(delay); }
																		catch (Exception InterruptedException) {}
																}
																masterMaze[location[0]][location[1]] = 42;
														}
														break;
												}
												try { TimeUnit.MILLISECONDS.sleep(delay); }
												catch (Exception InterruptedException) {}
										}
										masterMaze[location[0]][location[1]] = 42;
								}
								else if (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
										System.out.println("If: 12");
										//move east until wall
										while (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
												if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
														foundMiddle = true;
														break;
												}
												if (((!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) || (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18)) && masterMaze[location[0]][location[1]+1]!=16) {
														System.out.println("If: 13");
														if (!walls[0] && !walls[2]) {
																switch (dir.nextInt(2)) {
																		case 0:
																				if (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveNorth();
																						if (!validMove) { break; }
																						System.out.println("Moved North: 25");
																						location[0]--;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																				break;
																		case 1:
																				if (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveSouth();
																						if (!validMove) { break; }
																						System.out.println("Moved South: 26");
																						location[0]++;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																				break;
																}
														}
														else if (!walls[0]) {
																if (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
																		if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																				foundMiddle = true;
																				break;
																		}
																		if ((walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																				masterMaze[location[0]][location[1]] = 17;
																		}
																		else {
																				masterMaze[location[0]][location[1]] = wallIndex;
																		}
																		validMove = mouse.moveNorth();
																		if (!validMove) { break; }
																		System.out.println("Moved North: 27");
																		location[0]--;
																		masterMaze[location[0]][location[1]] = 42;
																		displayConstruct(masterMaze);
																		walls = mouse.checkWalls();
																		wallIndex = getWallIndex(walls);
																		try { TimeUnit.MILLISECONDS.sleep(delay); }
																		catch (Exception InterruptedException) {}
																}
																masterMaze[location[0]][location[1]] = 42;
														}
														else {
																if (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
																		if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																				foundMiddle = true;
																				break;
																		}
																		if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																				masterMaze[location[0]][location[1]] = 17;
																		}
																		else {
																				masterMaze[location[0]][location[1]] = wallIndex;
																		}
																		validMove = mouse.moveSouth();
																		if (!validMove) { break; }
																		System.out.println("Moved South: 28");
																		location[0]++;
																		masterMaze[location[0]][location[1]] = 42;
																		displayConstruct(masterMaze);
																		walls = mouse.checkWalls();
																		wallIndex = getWallIndex(walls);
																		try { TimeUnit.MILLISECONDS.sleep(delay); }
																		catch (Exception InterruptedException) {}
																}
																masterMaze[location[0]][location[1]] = 42;
														}
														break;
												}
												if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
														masterMaze[location[0]][location[1]] = 17;
												}
												else {
														masterMaze[location[0]][location[1]] = wallIndex;
												}
												validMove = mouse.moveEast();
												if (!validMove) { break; }
												System.out.println("Moved East: 29");
												location[1]++;
												masterMaze[location[0]][location[1]] = 42;
												displayConstruct(masterMaze);
												walls = mouse.checkWalls();
												wallIndex = getWallIndex(walls);
												try { TimeUnit.MILLISECONDS.sleep(delay); }
												catch (Exception InterruptedException) {}
										}
										masterMaze[location[0]][location[1]] = 42;
								}
								else if (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
										System.out.println("If: 14");
										//move south until wall
										while (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
												if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
														foundMiddle = true;
														break;
												}
												if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
														masterMaze[location[0]][location[1]] = 17;
												}
												else {
														masterMaze[location[0]][location[1]] = wallIndex;
												}
												validMove = mouse.moveSouth();
												if (!validMove) { break; }
												System.out.println("Moved South: 34");
												location[0]++;
												masterMaze[location[0]][location[1]] = 42;
												displayConstruct(masterMaze);
												walls = mouse.checkWalls();
												wallIndex = getWallIndex(walls);
												if (((!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) || (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18)) && masterMaze[location[0]+1][location[1]]!=16) {
														System.out.println("If: 15");
														if (!walls[1] && !walls[3]) {
																switch (dir.nextInt(2)) {
																		case 0:
																				if (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveEast();
																						if (!validMove) { break; }
																						System.out.println("Moved East: 30");
																						location[1]++;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																				break;
																		case 1:
																				if (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveWest();
																						if (!validMove) { break; }
																						System.out.println("Moved West: 31");
																						location[1]--;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																				break;
																}
														}
														else if (!walls[1]) {
																if (!walls[1] && masterMaze[location[0]][location[1]+1]!=17 && masterMaze[location[0]][location[1]+1]!=18) {
																		if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																				foundMiddle = true;
																				break;
																		}
																		if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																				masterMaze[location[0]][location[1]] = 17;
																		}
																		else {
																				masterMaze[location[0]][location[1]] = wallIndex;
																		}
																		validMove = mouse.moveEast();
																		if (!validMove) { break; }
																		System.out.println("Moved East: 32");
																		location[1]++;
																		masterMaze[location[0]][location[1]] = 42;
																		displayConstruct(masterMaze);
																		walls = mouse.checkWalls();
																		wallIndex = getWallIndex(walls);
																		try { TimeUnit.MILLISECONDS.sleep(delay); }
																		catch (Exception InterruptedException) {}
																}
																masterMaze[location[0]][location[1]] = 42;
														}
														else {
																if (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]][location[1]-1]!=18) {
																		if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																				foundMiddle = true;
																				break;
																		}
																		if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17)) {
																				masterMaze[location[0]][location[1]] = 17;
																		}
																		else {
																				masterMaze[location[0]][location[1]] = wallIndex;
																		}
																		validMove = mouse.moveWest();
																		if (!validMove) { break; }
																		System.out.println("Moved West: 33");
																		location[1]--;
																		masterMaze[location[0]][location[1]] = 42;
																		displayConstruct(masterMaze);
																		walls = mouse.checkWalls();
																		wallIndex = getWallIndex(walls);
																		try { TimeUnit.MILLISECONDS.sleep(delay); }
																		catch (Exception InterruptedException) {}
																}
																masterMaze[location[0]][location[1]] = 42;
														}
														break;
												}
												try { TimeUnit.MILLISECONDS.sleep(delay); }
												catch (Exception InterruptedException) {}
										}
										masterMaze[location[0]][location[1]] = 42;
								}
								else if (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
										System.out.println("If: 16");
										//move west until wall
										while (!walls[3] && masterMaze[location[0]][location[1]-1]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
												if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
														foundMiddle = true;
														break;
												}
												if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17)) {
														masterMaze[location[0]][location[1]] = 17;
												}
												else {
														masterMaze[location[0]][location[1]] = wallIndex;
												}
												validMove = mouse.moveWest();
												if (!validMove) { break; }
												System.out.println("Moved West: 39");
												location[1]--;
												masterMaze[location[0]][location[1]] = 42;
												displayConstruct(masterMaze);
												walls = mouse.checkWalls();
												wallIndex = getWallIndex(walls);
												if (((!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) || (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18)) && masterMaze[location[0]][location[1]-1]!=16) {
														System.out.println("If: 17");
														if (!walls[0] && !walls[2]) {
																switch (dir.nextInt(2)) {
																		case 0:
																				if (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveNorth();
																						if (!validMove) { break; }
																						System.out.println("Moved North: 35");
																						location[0]--;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																				break;
																		case 1:
																				if (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
																						if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																								foundMiddle = true;
																								break;
																						}
																						if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																								masterMaze[location[0]][location[1]] = 17;
																						}
																						else {
																								masterMaze[location[0]][location[1]] = wallIndex;
																						}
																						validMove = mouse.moveSouth();
																						if (!validMove) { break; }
																						System.out.println("Moved South: 36");
																						location[0]++;
																						masterMaze[location[0]][location[1]] = 42;
																						displayConstruct(masterMaze);
																						walls = mouse.checkWalls();
																						wallIndex = getWallIndex(walls);
																						try { TimeUnit.MILLISECONDS.sleep(delay); }
																						catch (Exception InterruptedException) {}
																				}
																				masterMaze[location[0]][location[1]] = 42;
																				break;
																}
														}
														else if (!walls[0]) {
																if (!walls[0] && masterMaze[location[0]-1][location[1]]!=17 && masterMaze[location[0]-1][location[1]]!=18) {
																		if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																				foundMiddle = true;
																				break;
																		}
																		if ((walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[2] || masterMaze[location[0]+1][location[1]]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																				masterMaze[location[0]][location[1]] = 17;
																		}
																		else {
																				masterMaze[location[0]][location[1]] = wallIndex;
																		}
																		validMove = mouse.moveNorth();
																		if (!validMove) { break; }
																		System.out.println("Moved North: 37");
																		location[0]--;
																		masterMaze[location[0]][location[1]] = 42;
																		displayConstruct(masterMaze);
																		walls = mouse.checkWalls();
																		wallIndex = getWallIndex(walls);
																		try { TimeUnit.MILLISECONDS.sleep(delay); }
																		catch (Exception InterruptedException) {}
																}
																masterMaze[location[0]][location[1]] = 42;
														}
														else {
																if (!walls[2] && masterMaze[location[0]+1][location[1]]!=17 && masterMaze[location[0]+1][location[1]]!=18) {
																		if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
																				foundMiddle = true;
																				break;
																		}
																		if ((walls[0] || masterMaze[location[0]-1][location[1]]==17) && (walls[1] || masterMaze[location[0]][location[1]+1]==17) && (walls[3] || masterMaze[location[0]][location[1]-1]==17)) {
																				masterMaze[location[0]][location[1]] = 17;
																		}
																		else {
																				masterMaze[location[0]][location[1]] = wallIndex;
																		}
																		validMove = mouse.moveSouth();
																		if (!validMove) { break; }
																		System.out.println("Moved South: 38");
																		location[0]++;
																		masterMaze[location[0]][location[1]] = 42;
																		displayConstruct(masterMaze);
																		walls = mouse.checkWalls();
																		wallIndex = getWallIndex(walls);
																		try { TimeUnit.MILLISECONDS.sleep(delay); }
																		catch (Exception InterruptedException) {}
																}
																masterMaze[location[0]][location[1]] = 42;
														}
														break;
												}
												try { TimeUnit.MILLISECONDS.sleep(delay); }
												catch (Exception InterruptedException) {}
										}
										masterMaze[location[0]][location[1]] = 42;
								}
						}
				}
				System.out.println("Found Middle!");
				System.out.println(mouse.duration);
				//Find the best path
		}
}
