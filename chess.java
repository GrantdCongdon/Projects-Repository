import java.util.Scanner;
public class chess {
        public static final String ANSI_RESET = "\u001B[0m";
        public static final String ANSI_BLACK = "\u001B[30m";
        public static final String ANSI_RED = "\u001B[31m";
        public static final String ANSI_GREEN = "\u001B[32m";
        public static final String ANSI_YELLOW = "\u001B[33m";
        public static final String ANSI_BLUE = "\u001B[34m";
        public static final String ANSI_PURPLE = "\u001B[35m";
        public static final String ANSI_CYAN = "\u001B[36m";
        public static final String ANSI_WHITE = "\u001B[37m";
        public static void printBoard(String[][] board) {
            //Coords to display for the user;s convience
            char[] lCoords = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'};
            int cc =  board.length; int qq=0;
            //Loops through the board rows reseting the variable qq each time
            for (int i=0; i<=board.length; i++) {
                qq=0;
                //loops through the columns
                for (int e=0; e<=board[0].length; e++) {
                    //if it is on the left then print a coordinate if its in between then just the chess pieces
                    if (e==0 && i<board.length) {
                        System.out.print("\033[31m");
                        System.out.print(cc+"\t");
                        System.out.print("\033[0");
                    }
                    if (i<board.length && e<board.length) {
                        System.out.print("\033[48;5;240m");
                        if ((int)board[i][e].charAt(0)==(int)'b') {
                            System.out.print("\033[30m");
                            System.out.print(board[i][e]+"\t");
                            System.out.print("\033[0m");
                        }
                        else if ((int)board[i][e].charAt(0)==(int)'w') {
                            System.out.print("\033[37m");
                            System.out.print(board[i][e]+"\t");
                            System.out.print("\033[0m");
                        }
                        else {
                            if (i%2==0 && e%2==0) {
                                System.out.print("\033[37m");
                                System.out.print(board[i][e]+"\t");
                                System.out.print("\033[0m");
                            }
                            else if (i%2==0 && e%2!=0) {
                                System.out.print("\033[30m");
                                System.out.print(board[i][e]+"\t");
                                System.out.print("\033[0m");
                            }
                            else if (i%2!=0 && e%2==0) {
                                System.out.print("\033[30m");
                                System.out.print(board[i][e]+"\t");
                                System.out.print("\033[0m");
                            }
                            else if (i%2!=0 && e%2!=0) {
                                System.out.print("\033[37m");
                                System.out.print(board[i][e]+"\t");
                                System.out.print("\033[0m");
                            }
                        }
                    }
                    //get alignment down for the bottom row and print out the bottom coordinates at the bottom of the board
                    if (e==0 && i==board.length) {
                        System.out.print("\033[0m");
                        System.out.print("\t");
                    }
                    else if (e>0 && i==board.length) {
                        System.out.print("\033[31m");
                        System.out.print(lCoords[qq]+"\t");
                        System.out.print("\033[0m");
                        qq++;
                    }
                }
                System.out.println("\n");
                cc--;
            }
        }
        public static int[] convert(String[][] board, String coord) {
        //Converts positions from traditional chess coordinates "a2" or "b7" to numerical coordinates in a (y, x) format
        int[] position = new int[2];
        for (int i=0; i<board.length; i++) {
                for (int e=0; e<board[0].length; e++) {
                        if (board[i][e].equals(coord)) {
                                position[0] = i; position[1]=e;
                                //Loops through all values of the board until it reaches the coordinate and record the value of the
                                //row and column, then enters that into an array
                        }
                }
        }
        return position;
    }
    public static int[] findTheKing(String[][] board, int color) {
        int[] position = new int[2];
        //Input the color of the King wanted, similar function to the method above, finds the King of the required color and returns
        //the numerical coordinates
        for (int i=0; i<board.length; i++) {
                for (int e=0; e<board[0].length; e++) {
                        if (board[i][e].equals("bK") && color==0) {
                                position[0] = i; position[1]=e;
                                //Scans for the string "bK" which is the code for Black King, then record the coordinates when found
                        }
                        else if (board[i][e].equals("wK") && color==1) {
                                position[0] = i; position[1]=e;
                                //Scans for the string "wK" which is the code for White King, then record the coordinates when found

                        }
                }
        }
        return position;
    }

    public static String convertToShorter(String userInput, char color) {
        //Shortens the step of converting the pawn to another piece when it reaches the end of the board
        String pieceValue = "";
        if(color=='w'){ //Runs only if the piece is white colored
            //Very repetitive, just converts the user input into the correct piece code, ex King to bK or wK depending on color
            if (userInput.equals("Queen") || userInput.equals("queen")) { //If the user inputs the piece lowercase or uppercase, then it still works
                pieceValue = "wQ";
            }
            else if (userInput.equals("Bishop") || userInput.equals("bishop")) {
                pieceValue = "wB";
            }
            else if (userInput.equals("Knight") || userInput.equals("knight")) {
                pieceValue = "wH";
            }
            else if (userInput.equals("Rook") || userInput.equals("rook")) {
                pieceValue = "wR";
            }
            else if (userInput.equals("Pawn") || userInput.equals("pawn")) {
                pieceValue = "wP";
            }
        }
        if(color=='b'){ //Same as above, just for black pieces
            if (userInput.equals("Queen") || userInput.equals("queen")) {
                pieceValue = "bQ";
            }
            else if (userInput.equals("Bishop") || userInput.equals("bishop")) {
                pieceValue = "bB";
            }
            else if (userInput.equals("Knight") || userInput.equals("knight")) {
                pieceValue = "bH";
            }
            else if (userInput.equals("Rook") || userInput.equals("rook")) {
                pieceValue = "bR";
            }
            else if (userInput.equals("Pawn") || userInput.equals("pawn")) {
                pieceValue = "bP";
            }
        }
    return pieceValue;
    }
    public static boolean compareArrays(String[][] array1, String[][] array2) {
        //Takes two arrays and compares all of their values to see if they are identical, if they are it returns true
        boolean match = true;
        for (int i=0; i<array1.length; i++) {
            for (int e=0; e<array1[0].length; e++) {
                if (!array1[i][e].equals(array2[i][e])) { match = false; }
                //Loops through the columns and rows, i and e, and if the values at a vertex aren't identical, the value is changed to false, and later returned
            }
        }
        return match;
    }
    public static String[][] copyArray(String[][] original) {
        //Basic function, takes an array and makes an exact copy of it, which it returns
        String[][] copy = new String[original.length][original[0].length];
        //Makes a new array with the same size as the original
        for (int i=0; i<original.length; i++) {
            for (int e=0; e<original[0].length; e++) {
                copy[i][e] = original[i][e];
                //Loops through each column and row of the original array, i and e, and copies each value to the new array
            }
        }
        return copy;
    }
    public static String[][] pawn(String[][] board, String[][] coordBoard, String position, String proposedCoord) {
        int[] nPosition = convert(coordBoard, position);
        int[] nProposedCoord = convert(coordBoard, proposedCoord);
        //Converts the initial position of the pawn to numerical values, and the same with the position the user wanted to move the pawn into
        int top = nPosition[0] > 0 ? nPosition[0] - 1: -1;
        int bottom = nPosition[0] < board.length ? nPosition[0] + 1: board.length;
        int right = nPosition[1] < board.length ? nPosition[1] + 1: board.length;
        int left = nPosition[1] > 0 ? nPosition[1] - 1: -1;
        //Determines the coordinates of all the locations around the pawn to all for movement
        if ((top==-1 && top==nProposedCoord[0]) || (bottom==board.length && bottom==nProposedCoord[0]) || (right==board.length && right==nProposedCoord[1]) || (left==-1 && left==nProposedCoord[1])) { return board; }
        //Conditions which would make the move invalid: If the piece tries to move up when at the top of the board, if the piece tries to move down from the bottom row,
        //If the piece is on the right edge and tries to move right more, or if it's on the left edge and tries to move left more
        char piece = (board[nPosition[0]][nPosition[1]]).charAt(0);
        //Determines the color of the piece in question
        if ((int)piece==(int)'b') {
            if (bottom<board.length) { //If moving down is a valid move
                if (board[bottom][nPosition[1]].equals("-") && bottom==nProposedCoord[0] && nPosition[1]==nProposedCoord[1]) {
                //If the space below if open (has a "-") and the user wants to move downward
                    if (bottom==board.length-1) {
                    //If the pawn is moving downward into the bottom row, meaning it can change into another piece
                        Scanner r = new Scanner(System.in);
                        System.out.print("Enter what you want to pawn to be turned into: ");
                        String character = r.nextLine();
                        //Asks the user for the new piece, then converts into the piece code and then places it on the board, then opens the previous spot
                        board[bottom][nPosition[1]] = convertToShorter(character, piece);
                        board[nPosition[0]][nPosition[1]] = "-";
                    }
                    else {
                    //If the pawn isn't moving to the opposite end, it just moves as normal
                        board[bottom][nPosition[1]] = "bP";
                        board[nPosition[0]][nPosition[1]] = "-";
                    }
                }
                else if (board[bottom][nPosition[1]].equals("-") && bottom+1==nProposedCoord[0] && nPosition[1]==nProposedCoord[1] && board[bottom+1][nPosition[1]].equals("-") && nPosition[0]==1) {
                    //If the pawn is moving 2 places because it's the first time it's moved
                    //If the pawn can move down, and moving down 2 is what is requested, and the column stays the same, and the space 2 away is free, and it hasn't moved yet
                    board[bottom+1][nPosition[1]] = "bP";
                    board[nPosition[0]][nPosition[1]] = "-";
                }
            }
            if (bottom<board.length && right<board[0].length) {
                //If it can move down and right without moving off the board
                if (!board[bottom][right].equals("-") && (int)(board[bottom][right]).charAt(0)==(int)'w' && bottom==nProposedCoord[0] && right==nProposedCoord[1]) {
                //For taking pieces with a pawn, if the space to the bottom right isn't empty, and the piece there is white, and the user wants the piece to move there
                    if (bottom==board.length-1) {
                        //If the piece is being taken on the bottom row, meaning the pawn could change form, ask what to turn into
                        Scanner r = new Scanner(System.in);
                        System.out.print("Enter what you want to pawn to be turned into: ");
                        String character = r.nextLine();
                        board[bottom][right] = convertToShorter(character, piece);
                        board[nPosition[0]][nPosition[1]] = "-";
                        }
                    else {
                        //If it's not going to the bottom row, move to the spot normally and empty the previous space
                        board[bottom][right] = "bP";
                        board[nPosition[0]][nPosition[1]] = "-";
                    }
                }
            }
            if (bottom<board.length && left>=0) {
                //If it can move down and left without moving off the board
                if (!board[bottom][left].equals("-") && (int)(board[bottom][left]).charAt(0)==(int)'w' && bottom==nProposedCoord[0] && left==nProposedCoord[1]) {
                //For taking pieces with a pawn, if the space to the bottom left isn't empty, and the piece there is white, and the user wants the piece to move there
                    if (bottom==board.length-1) {
                        //If the piece is being taken on the bottom row, meaning the pawn could change form, ask what to turn into
                        Scanner r = new Scanner(System.in);
                        System.out.print("Enter what you want to pawn to be turned into: ");
                        String character = r.nextLine();
                        //Replace the pawn with the new piece and empty the old space
                        board[bottom][left] = convertToShorter(character, piece);
                        board[nPosition[0]][nPosition[1]] = "-";
                    }
                    else {
                        //If it's not going to the bottom row, move to the spot normally and empty the previous space
                        board[bottom][left] = "bP";
                        board[nPosition[0]][nPosition[1]] = "-";
                    }
                }
            }
        }
        else if ((int)piece==(int)'w') {
            //Same logic as above, except the pawns are moving up instead of down
            if (top>=0) {
                if (board[top][nPosition[1]].equals("-") && top==nProposedCoord[0] && nPosition[1]==nProposedCoord[1]) {
                    if (top==0) {
                        Scanner r = new Scanner(System.in);
                        System.out.print("Enter what you want to pawn to be turned into: ");
                        String character = r.nextLine();
                        board[top][nPosition[1]] = convertToShorter(character, piece);
                        board[nPosition[0]][nPosition[1]] = "-";
                    }
                    else {
                        board[top][nPosition[1]] = "wP";
                        board[nPosition[0]][nPosition[1]] = "-";
                    }
                }
                else if (board[top][nPosition[1]].equals("-") && top-1==nProposedCoord[0] && nPosition[1]==nProposedCoord[1] && board[top-1][nPosition[1]].equals("-") && nPosition[0]==6) {
                    board[top-1][nPosition[1]] = "wP";
                    board[nPosition[0]][nPosition[1]] = "-";
                }
            }
            if (top>=0 && right<board.length) {
                if (!board[top][right].equals("-") && (int)(board[top][right]).charAt(0)==(int)'b' && top==nProposedCoord[0] && right==nProposedCoord[1]) {
                    if (top==0) {
                        Scanner r = new Scanner(System.in);
                        System.out.print("Enter what you want to pawn to be turned into: ");
                        String character = r.nextLine();
                        board[top][right] = convertToShorter(character, piece);
                        board[nPosition[0]][nPosition[1]] = "-";
                    }
                    else {
                        board[top][right] = "wP";
                        board[nPosition[0]][nPosition[1]] = "-";
                    }
                }
            }
            if (top>=0 && left>=0) {
               if (!board[top][left].equals("-") && (int)(board[top][left]).charAt(0)==(int)'b' && top==nProposedCoord[0] && left==nProposedCoord[1]) {
                    if (top==0) {
                        Scanner r = new Scanner(System.in);
                        System.out.print("Enter what you want to pawn to be turned into: ");
                        String character = r.nextLine();
                        board[top][left] = convertToShorter(character, piece);
                        board[nPosition[0]][nPosition[1]] = "-";
                    }
                    else {
                        board[top][left] = "wP";
                        board[nPosition[0]][nPosition[1]] = "-";
                    }
                }
            }
        }
        return board;
    }
    public static String[][] rook(String[][] board, String[][] coordBoard, String position, String proposedCoord, int rookMoves) {
        int[] nPosition = convert(coordBoard, position);
        int[] nProposedCoord = convert(coordBoard, proposedCoord);
        //Converts the input coordinates into the (y, x), and stores those coordinates, nPosition for start and nProposedCoord for end
        char piece = (board[nPosition[0]][nPosition[1]]).charAt(0);
        //Gets the color of the piece in question
        boolean validPosition = false;
        int row = nPosition[0]; int column = nPosition[1]; int loop=0;
        while (row>=0) {
            if (row==nProposedCoord[0] && column==nProposedCoord[1]) { //If the piece makes it to the final position without the loop exiting
                validPosition = true;
                break;
                //If the while loop makes it to the final position, while going down, then it returns that the move is valid
            }
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            //If there is a space that isn't empty inbetween the start and target space, then the loops breaks and the move is invalid
            row--; loop++;
            //Each loop it decreases the row, and increases the number of times looped
        }
        row = nPosition[0]; loop=0;
        while (row<board.length) {
            if (row==nProposedCoord[0] && column==nProposedCoord[1]) { //If the piece makes it to the final position without the loop exiting
                validPosition = true;
                break;
                //If the while loop makes it to the final position, while going up, then it returns that the move is valid
            }
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            //If there is a space that isn't empty (has a letter) inbetween the start and target space, then the loops breaks and the move is invalid, given that it isn't the start position
            row++; loop++;
            //Each loop it increases the row, and increases the number of times looped

        }
        row = nPosition[0]; column = nPosition[1]; loop=0;
        //Resets all the values so it can check more movements
        while (column<board[0].length) { //While the column is still a valid position in the array
        //Same logic as the above loops for the columns, except it's checking whether the rook can move left or right instead of up or down
            if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
                validPosition = true;
                break;
            }
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            column++; loop++;
        }
        column = nPosition[1]; loop=0;
        while (column>=0) {
            if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
                validPosition = true;
                break;
            }
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            column--; loop++;
        }
        //End of repeat logic
        if (validPosition && (int)piece==(int)'b' && (board[nProposedCoord[0]][nProposedCoord[1]].equals("-") || (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)==(int)'w')) {
            //If the spaces to get to the end position from the start are empty, and the piece is black, and the end space is empty or has a white piece, move the piece to that space and empty the old space
            board[nProposedCoord[0]][nProposedCoord[1]] = "bR";
            board[nPosition[0]][nPosition[1]] = "-";
            rookMoves++;
            //Increases a counter used for castleing
        }
        else if (validPosition && (int)piece==(int)'w' && (board[nProposedCoord[0]][nProposedCoord[1]].equals("-") || (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)==(int)'b')) {
            //Same logic as the above if statement, except for white pieces, so it checks to see if the end space is empty or has a black piece
            board[nProposedCoord[0]][nProposedCoord[1]] = "wR";
            board[nPosition[0]][nPosition[1]] = "-";
            rookMoves++;
            //Increases a counter used for castleing
        }
        return board;
    }
    public static String[][] knight(String[][] board, String[][] coordBoard, String position, String proposedCoord) {
        int[] nPosition = convert(coordBoard, position);
        int[] nProposedCoord = convert(coordBoard, proposedCoord);
        //Converts the input coordinates into the (y, x), and stores those coordinates, nPosition for start and nProposedCoord for end
        int topRightY = nPosition[0]-2;
        int topRightX = nPosition[1]+1;
        int topLeftY = nPosition[0]-2;
        int topLeftX = nPosition[1]-1;
        int bottomRightY = nPosition[0]+2;
        int bottomRightX = nPosition[1]+1;
        int bottomLeftY = nPosition[0]+2;
        int bottomLeftX = nPosition[1]-1;
        int rightTopY = nPosition[0]-1;
        int rightTopX = nPosition[1]+2;
        int rightBottomY = nPosition[0]+1;
        int rightBottomX = nPosition[1]+2;
        int leftTopY = nPosition[0]-1;
        int leftTopX = nPosition[1]-2;
        int leftBottomY = nPosition[0]+1;
        int leftBottomX = nPosition[1]-2;
        //Creates variables for all 8 possible moves that the Knight could concieveably make
        if ((topRightY<0 && topRightY==nProposedCoord[0]) || (topRightX>=board[0].length && topRightX==nProposedCoord[1]) ||
            (topLeftY<0 && topLeftY==nProposedCoord[0]) || (topLeftX<0 && topLeftX==nProposedCoord[1]) ||
            (bottomRightY>=board.length && bottomRightY==nProposedCoord[0]) || (bottomRightX>=board[0].length && bottomRightX==nProposedCoord[1]) ||
            (bottomLeftY>=board.length && bottomLeftY==nProposedCoord[0]) || (bottomLeftX<0 && bottomLeftX==nProposedCoord[1]) ||
            (rightTopY<0 && rightTopY==nProposedCoord[0]) || (rightTopX>=board[0].length && rightTopX==nProposedCoord[1]) ||
            (rightBottomY>=board.length && rightBottomY==nProposedCoord[0]) || (rightBottomX>=board[0].length && rightBottomX==nProposedCoord[1]) ||
            (leftTopY<0 && leftTopX==nProposedCoord[0]) || (leftTopX<0 && leftTopX==nProposedCoord[1]) ||
            (leftBottomY>=board.length && leftBottomY==nProposedCoord[0]) || (leftBottomX<0 && leftBottomX==nProposedCoord[1])) { return board; }
            //Checks the validity of all of the possible moves that the knight could make, and if they are desired, if the desired position is invalid, it resets
        char piece = (board[nPosition[0]][nPosition[1]]).charAt(0);
        //Gets the color of the piece in question
        if ((int)piece==(int)'b' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'b') { //If the piece is black, and the target position doesn't have a black piece in it
            if (topRightY==nProposedCoord[0] && topRightX==nProposedCoord[1]) { //Now that is move is known valid, move the piece and empty the start position
                board[topRightY][topRightX] = "bH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (topLeftY==nProposedCoord[0] && topLeftX==nProposedCoord[1]) { //Same as above
                board[topLeftY][topLeftX] = "bH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (bottomRightY==nProposedCoord[0] && bottomRightX==nProposedCoord[1]) { //Same as above
                board[bottomRightY][bottomRightX] = "bH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (bottomLeftY==nProposedCoord[0] && bottomLeftX==nProposedCoord[1]) { //Same as above
                board[bottomLeftY][bottomLeftX] = "bH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (rightTopY==nProposedCoord[0] && rightTopX==nProposedCoord[1]) { //Same as above
                board[rightTopY][rightTopX] = "bH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (rightBottomY==nProposedCoord[0] && rightBottomX==nProposedCoord[1]) { //Same as above
                board[rightBottomY][rightBottomX] = "bH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (leftTopX==nProposedCoord[0] && leftTopX==nProposedCoord[1]) { //Same as above
                board[leftTopY][leftTopX] = "bH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (leftBottomY==nProposedCoord[0] && leftBottomX==nProposedCoord[1]) { //Same as above
                board[leftBottomY][leftBottomX] = "bH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
        }
        else if ((int)piece==(int)'w' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'w') { //Same logic as above is statement, except that it applies to white pieces
            if (topRightY==nProposedCoord[0] && topRightX==nProposedCoord[1]) { //Same logic, just for white
                board[topRightY][topRightX] = "wH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (topLeftY==nProposedCoord[0] && topLeftX==nProposedCoord[1]) { //Same as above
                board[topLeftY][topLeftX] = "wH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (bottomRightY==nProposedCoord[0] && bottomRightX==nProposedCoord[1]) { //Same as above
                board[bottomRightY][bottomRightX] = "wH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (bottomLeftY==nProposedCoord[0] && bottomLeftX==nProposedCoord[1]) { //Same as above
                board[bottomLeftY][bottomLeftX] = "wH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (rightTopY==nProposedCoord[0] && rightTopX==nProposedCoord[1]) { //Same as above
                board[rightTopY][rightTopX] = "wH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (rightBottomY==nProposedCoord[0] && rightBottomX==nProposedCoord[1]) { //Same as above
                board[rightBottomY][rightBottomX] = "wH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (leftTopX==nProposedCoord[0] && leftTopX==nProposedCoord[1]) { //Same as above
                board[leftTopY][leftTopX] = "wH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
            else if (leftBottomY==nProposedCoord[0] && leftBottomX==nProposedCoord[1]) { //Same as above
                board[leftBottomY][leftBottomX] = "wH";
                board[nPosition[0]][nPosition[1]] = "-";
            }
        }
        //Returns an updated board
        return board;
    }
    public static String[][] bishop(String[][] board, String[][] coordBoard, String position, String proposedCoord) {
        int[] nPosition = convert(coordBoard, position);
        int[] nProposedCoord = convert(coordBoard, proposedCoord);
        //Converts the input coordinates into the (y, x), and stores those coordinates, nPosition for start and nProposedCoord for end
        char piece = (board[nPosition[0]][nPosition[1]]).charAt(0);
        //Gets the color of the piece
        boolean validPosition = false;
        int row = nPosition[0];
        int column = nPosition[1];
        int loop=0;
        //Creates variables that are needed to check the validity of the move
        while (row>=0 && column<board[0].length) { //While the row and colum are valid
            if (row==nProposedCoord[0] && column==nProposedCoord[1]) { //If the loop gets to the desired location it sets the move validity to true
                validPosition = true;
                break;
            }
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; } //If a space between the start and final location has a piece, the move is invalid, given that it isn't the original position
            row--; column++; loop++;
            //If neither is true, it moves up and to the right and checks again
        }
        row = nPosition[0]; column = nPosition[1]; loop=0; //Resets the variables used
        while (row<board.length && column<board[0].length) { //While the location being checked is on the board, same logic as above but for down and right
            if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
                validPosition = true;
                break;
            }
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            row++; column++; loop++;
        }
        row = nPosition[0]; column = nPosition[1]; loop=0;//Resets the variables used
        while (row<board.length && column>=0) {//While the location being checked is on the board, same logic as above but for down and left
            if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
                validPosition = true;
                break;
            }
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            row++; column--; loop++;
        }
        row = nPosition[0]; column = nPosition[1]; loop=0;//Resets the variables used
        while (row>=0 && column>=0) {//While the location being checked is on the board, same logic as above but for up and left
            if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
                validPosition = true;
                break;
            }
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            row--; column--; loop++;
        }
        if (validPosition && (int)piece==(int)'b' && (board[nProposedCoord[0]][nProposedCoord[1]].equals("-") || (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)==(int)'w')) {
            //If the position is valid, and the piece is black, and the target position is empty or has a white piece
            board[nProposedCoord[0]][nProposedCoord[1]] = "bB";
            board[nPosition[0]][nPosition[1]] = "-";
            //Moves the piece and empties the old space
        }
        else if (validPosition && (int)piece==(int)'w' && (board[nProposedCoord[0]][nProposedCoord[1]].equals("-") || (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)==(int)'b')) {
            //If the position is valid, and the piece is white, and the target position is empty or has a black piece
            board[nProposedCoord[0]][nProposedCoord[1]] = "wB";
            board[nPosition[0]][nPosition[1]] = "-";
            //Moves the piece and empties the old space
        }
        return board;
    }
	public static String[][] queen(String[][] board, String[][] coordBoard, String position, String proposedCoord) {
        //converts standard coords to usable ones
		int[] nPosition = convert(coordBoard, position);
		int[] nProposedCoord = convert(coordBoard, proposedCoord);
        //Gets the peice
		char piece = (board[nPosition[0]][nPosition[1]]).charAt(0);
		boolean validPosition = false;
		//Rook Like Movements, same logic as that class
		int row = nPosition[0]; int column = nPosition[1]; int loop=0;
		while (row>=0) {
			if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
				validPosition = true;
				break;
			}
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            row--; loop++;
		}
		row = nPosition[0]; loop=0;
		while (row<board.length) {
			if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
				validPosition = true;
				break;
			}
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            row++; loop++;
		}
		row = nPosition[0]; column = nPosition[1]; loop=0;
		while (column<board[0].length) {
			if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
				validPosition = true;
				break;
			}
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            column++; loop++;
		}
		column = nPosition[1]; loop=0;
		while (column>=0) {
			if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
				validPosition = true;
				break;
			}
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            column--; loop++;
		}
		//Bishop Like Movements, same logic as that class
		row = nPosition[0]; column = nPosition[1]; loop=0;
		while (row>=0 && column<board[0].length) {
			if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
				validPosition = true;
				break;
			}
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            row--; column++; loop++;
		}
		row = nPosition[0]; column = nPosition[1]; loop=0;
		while (row<board.length && column<board[0].length) {
			if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
				validPosition = true;
				break;
			}
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            row++; column++; loop++;
		}
		row = nPosition[0]; column = nPosition[1]; loop=0;
		while (row<board.length && column>=0) {
			if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
				validPosition = true;
				break;
			}
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            row++; column--; loop++;
		}
		row = nPosition[0]; column = nPosition[1]; loop=0;
		while (row>=0 && column>=0) {
			if (row==nProposedCoord[0] && column==nProposedCoord[1]) {
				validPosition = true;
				break;
			}
            if (((int)board[row][column].charAt(0)==(int)'b' || (int)board[row][column].charAt(0)==(int)'w') && loop>0) { break; }
            row--; column--; loop++;
		}
		if (validPosition && (int)piece==(int)'b' && (board[nProposedCoord[0]][nProposedCoord[1]].equals("-") || (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)==(int)'w')) {
			board[nProposedCoord[0]][nProposedCoord[1]] = "bQ";
            board[nPosition[0]][nPosition[1]] = "-";
		}
		else if (validPosition && (int)piece==(int)'w' && (board[nProposedCoord[0]][nProposedCoord[1]].equals("-") || (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)==(int)'b')) {
			board[nProposedCoord[0]][nProposedCoord[1]] = "wQ";
            board[nPosition[0]][nPosition[1]] = "-";
		}
		return board;
	}
	public static String[][] king(String[][] board, String[][] coordBoard, String position, String proposedCoord, int kingMoves, int rookMoves) {
        //Get the coords to numerical values
		int[] nPosition = convert(coordBoard, position);
		int[] nProposedCoord = convert(coordBoard, proposedCoord);
        //get the values for the top, bottom, left, and right coordinate
		int top = nPosition[0] > 0 ? nPosition[0] - 1: -1;
		int bottom = nPosition[0] < board.length ? nPosition[0] + 1: board.length;
		int right = nPosition[1] < board.length ? nPosition[1] + 1: board.length;
		int left = nPosition[1] > 0 ? nPosition[1] - 1: -1;
        //If they are trying to move to an invalid stop then end it here
		if ((top==-1 && top==nProposedCoord[0]) || (bottom==board.length && bottom==nProposedCoord[0]) || (right==board.length && right==nProposedCoord[1]) || (left==-1 && left==nProposedCoord[1])) { return board; }
        //get which side the peice is
		char piece = (board[nPosition[0]][nPosition[1]]).charAt(0);
        //castling logic
        //check if the piece selected is black and where they want to go is not black and the king hasn't moved yet and the rook hasn't moved yet y user wants be there
        if ((int)piece==(int)'b' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'b' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'w' && kingMoves==0 && rookMoves==0 && nProposedCoord[0]==nPosition[0] && nProposedCoord[1]==right+1) {
            //make sure the king is not in check, and the spot where it is going is not in check and the spot its crossing over is not in check
            if (!check(board, coordBoard, 'b') && !spotCheck(board, coordBoard, coordBoard[nProposedCoord[0]][nProposedCoord[1]], 'b') && !spotCheck(board, coordBoard, coordBoard[nProposedCoord[0]][nProposedCoord[1]+1], 'b')) {
                //move the king and rook and reset the peices
                board[nProposedCoord[0]][nProposedCoord[1]] = "bK";
                board[nProposedCoord[0]][nProposedCoord[1]-1] = "bR";
                board[nPosition[0]][nPosition[1]] = "-";
                board[0][7] = "-";
                //a king move based on the rules
                kingMoves++;
            }
        }
        //Same logic as ^ but on the other side of the king
        else if ((int)piece==(int)'b' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'b' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'w' && kingMoves==0 && rookMoves==0 && nProposedCoord[0]==nPosition[0] && nProposedCoord[1]==left-1) {
            if (!check(board, coordBoard, 'b') && !spotCheck(board, coordBoard, coordBoard[nProposedCoord[0]][nProposedCoord[1]], 'b') && !spotCheck(board, coordBoard, board[nProposedCoord[0]][nProposedCoord[1]-1], 'b')) {
                board[nProposedCoord[0]][nProposedCoord[1]] = "bK";
                board[nProposedCoord[0]][nProposedCoord[1]+1] = "bR";
                board[nPosition[0]][nPosition[1]] = "-";
                board[0][0] = "-";
                kingMoves++;
            }
        }
        //Same logic but for the white king and its castling logic
        else if ((int)piece==(int)'w' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'w' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'b' && kingMoves==0 && rookMoves==0 && nProposedCoord[0]==nPosition[0] && nProposedCoord[1]==right+1) {
            if (!check(board, coordBoard, 'w') && !spotCheck(board, coordBoard, coordBoard[nProposedCoord[0]][nProposedCoord[1]], 'w') && !spotCheck(board, coordBoard, board[nProposedCoord[0]][nProposedCoord[1]+1], 'w')) {
                board[nProposedCoord[0]][nProposedCoord[1]] = "wK";
                board[nProposedCoord[0]][nProposedCoord[1]-1] = "wR";
                board[nPosition[0]][nPosition[1]] = "-";
                board[7][7] = "-";
                kingMoves++;
            }
            if (spotCheck(board, coordBoard, coordBoard[nProposedCoord[0]][nProposedCoord[1]], 'w')) { System.out.print("Y"); }
        }
        //Other side of white
        else if ((int)piece==(int)'w' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'w' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'b' && kingMoves==0 && rookMoves==0 && nProposedCoord[0]==nPosition[0] && nProposedCoord[1]==left-1) {
            if (!check(board, coordBoard, 'w') && !spotCheck(board, coordBoard, coordBoard[nProposedCoord[0]][nProposedCoord[1]], 'w') && !spotCheck(board, coordBoard, board[nProposedCoord[0]][nProposedCoord[1]-1], 'w')) {
                board[nProposedCoord[0]][nProposedCoord[1]] = "wK";
                board[nProposedCoord[0]][nProposedCoord[1]+1] = "wR";
                board[nPosition[0]][nPosition[1]] = "-";
                board[7][0] = "-";
                kingMoves++;
            }
        }
        //If its not trying to castle, making sure that the spots its moving to is not the same color as the piece
		else if ((int)piece==(int)'b' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'b') {
            //Go through all the possible spots that the king can move and move if they are valid and the user wants to move there
			if (top==nProposedCoord[0] && left==nProposedCoord[1]) {
				board[top][left] = "bK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (top==nProposedCoord[0] && nPosition[1]==nProposedCoord[1]) {
				board[top][nPosition[1]] = "bK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (top==nProposedCoord[0] && right==nProposedCoord[1]) {
				board[top][right] = "bK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (nPosition[0]==nProposedCoord[0] && right==nProposedCoord[1]) {
				board[nPosition[0]][right] = "bK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (bottom==nProposedCoord[0] && right==nProposedCoord[1]) {
				board[bottom][right] = "bK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (bottom==nProposedCoord[0] && nPosition[1]==nProposedCoord[1]) {
				board[bottom][nPosition[1]] = "bK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (bottom==nProposedCoord[0] && left==nProposedCoord[1]) {
				board[bottom][left] = "bK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (nPosition[0]==nProposedCoord[0] && left==nProposedCoord[1]) {
				board[nPosition[0]][left] = "bK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
		}
        //Same logic as above but for white king instead
		else if ((int)piece==(int)'w' && (int)(board[nProposedCoord[0]][nProposedCoord[1]]).charAt(0)!=(int)'w') {
			if (top==nProposedCoord[0] && left==nProposedCoord[1]) {
				board[top][left] = "wK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (top==nProposedCoord[0] && nPosition[1]==nProposedCoord[1]) {
				board[top][nPosition[1]] = "wK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (top==nProposedCoord[0] && right==nProposedCoord[1]) {
				board[top][right] = "wK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (nPosition[0]==nProposedCoord[0] && right==nProposedCoord[1]) {
				board[nPosition[0]][right] = "wK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (bottom==nProposedCoord[0] && right==nProposedCoord[1]) {
				board[bottom][right] = "wK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (bottom==nProposedCoord[0] && nPosition[1]==nProposedCoord[1]) {
				board[bottom][nPosition[1]] = "wK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (bottom==nProposedCoord[0] && left==nProposedCoord[1]) {
				board[bottom][left] = "wK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
			else if (nPosition[0]==nProposedCoord[0] && left==nProposedCoord[1]) {
				board[nPosition[0]][left] = "wK";
                board[nPosition[0]][nPosition[1]] = "-";
                kingMoves++;
			}
		}
        //return if the updated board
		return board;
	}
	public static boolean check(String[][] board, String[][] coordBoard, char side) {
        //find the cordinates of the kings
		int[] blackKingCoords = findTheKing(board, 0);
		int[] whiteKingCoords = findTheKing(board, 1);
        //Loops through all the peices on the board
		for (int row=0; row<board.length; row++) {
			for (int column=0; column<board[0].length; column++) {
                //as long as the position is not empty, try to move that peice, depending on what peice it is, to the king and if any peice can move there and it is
                //of the opposite team then that king is in check
				if (!(board[row][column]).equals("-")) {
					if ((int)(board[row][column]).charAt(1)==(int)'K') {
						String[][] newBoardBlack = copyArray(board);
                        king(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[blackKingCoords[0]][blackKingCoords[1]], 1, 1);
						String[][] newBoardWhite = copyArray(board);
                        king(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[whiteKingCoords[0]][whiteKingCoords[1]], 1, 1);
						if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
						else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
					}
					else if ((int)(board[row][column]).charAt(1)==(int)'Q') {
                        String[][] newBoardBlack = copyArray(board);
                        queen(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[blackKingCoords[0]][blackKingCoords[1]]);
                        String[][] newBoardWhite = copyArray(board);
                        queen(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[whiteKingCoords[0]][whiteKingCoords[1]]);
						if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
						else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
					}
					else if ((int)(board[row][column]).charAt(1)==(int)'B') {
                        String[][] newBoardBlack = copyArray(board);
                        bishop(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[blackKingCoords[0]][blackKingCoords[1]]);
                        String[][] newBoardWhite = copyArray(board);
                        bishop(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[whiteKingCoords[0]][whiteKingCoords[1]]);
						if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
						else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
					}
					else if ((int)(board[row][column]).charAt(1)==(int)'H') {
                        String[][] newBoardBlack = copyArray(board);
                        knight(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[blackKingCoords[0]][blackKingCoords[1]]);
                        String[][] newBoardWhite = copyArray(board);
                        knight(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[whiteKingCoords[0]][whiteKingCoords[1]]);
						if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
						else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
					}
					else if ((int)(board[row][column]).charAt(1)==(int)'R') {
                        String[][] newBoardBlack = copyArray(board);
                        rook(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[blackKingCoords[0]][blackKingCoords[1]], 1);
                        String[][] newBoardWhite = copyArray(board);
                        rook(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[whiteKingCoords[0]][whiteKingCoords[1]], 1);
						if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
						else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
					}
					else if ((int)(board[row][column]).charAt(1)==(int)'P') {
                        String[][] newBoardBlack = copyArray(board);
                        pawn(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[blackKingCoords[0]][blackKingCoords[1]]);
                        String[][] newBoardWhite = copyArray(board);
                        pawn(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[whiteKingCoords[0]][whiteKingCoords[1]]);
						if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
						else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
					}
				}
			}
		}
        //if no peices can move to the king then there is no check
		return false;
	}
    public static boolean spotCheck(String[][] board, String[][] coordBoard, String position, char side) {
        //Spot check has the same logic as check, the only difference being that spotcheck checks if any peice can go to a specicific spot rather than the king coords
        int[] nPosition = convert(coordBoard, position);
        for (int row=0; row<board.length; row++) {
            for (int column=0; column<board[0].length; column++) {
                if (!(board[row][column]).equals("-")) {
                    if ((int)(board[row][column]).charAt(1)==(int)'K') {
                        String[][] newBoardBlack = copyArray(board);
                        king(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]], 1, 1);
                        String[][] newBoardWhite = copyArray(board);
                        king(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]], 1, 1);
                        if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
                        else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
                    }
                    else if ((int)(board[row][column]).charAt(1)==(int)'Q') {
                        String[][] newBoardBlack = copyArray(board);
                        queen(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]]);
                        String[][] newBoardWhite = copyArray(board);
                        queen(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]]);
                        if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
                        else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
                    }
                    else if ((int)(board[row][column]).charAt(1)==(int)'B') {
                        String[][] newBoardBlack = copyArray(board);
                        bishop(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]]);
                        String[][] newBoardWhite = copyArray(board);
                        bishop(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]]);
                        if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
                        else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
                    }
                    else if ((int)(board[row][column]).charAt(1)==(int)'H') {
                        String[][] newBoardBlack = copyArray(board);
                        knight(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]]);
                        String[][] newBoardWhite = copyArray(board);
                        knight(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]]);
                        if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
                        else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
                    }
                    else if ((int)(board[row][column]).charAt(1)==(int)'R') {
                        String[][] newBoardBlack = copyArray(board);
                        rook(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]], 1);
                        String[][] newBoardWhite = copyArray(board);
                        rook(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]], 1);
                        if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
                        else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
                    }
                    else if ((int)(board[row][column]).charAt(1)==(int)'P') {
                        String[][] newBoardBlack = copyArray(board);
                        pawn(newBoardBlack, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]]);
                        String[][] newBoardWhite = copyArray(board);
                        pawn(newBoardWhite, coordBoard, coordBoard[row][column], coordBoard[nPosition[0]][nPosition[1]]);
                        if (!compareArrays(board, newBoardBlack) && (int)side==(int)'b') { return true; }
                        else if (!compareArrays(board, newBoardWhite) && (int)side==(int)'w') { return true; }
                    }
                }
            }
        }
        return false;
    }
    public static boolean stalemate(String[][] board, String[][] coordBoard, char side) {
        //Find the position of the kings
        int[] blackKingCoords = findTheKing(board, 0);
        int[] whiteKingCoords = findTheKing(board, 1);
        //Get the locations of all the posibile places where a peice could go around the knigns
        int topBlack = blackKingCoords[0] > 0 ? blackKingCoords[0] - 1: -1;
        int bottomBlack = blackKingCoords[0] < board.length ? blackKingCoords[0] + 1: board.length;
        int rightBlack = blackKingCoords[1] < board.length ? blackKingCoords[1] + 1: board.length;
        int leftBlack = blackKingCoords[1] > 0 ? blackKingCoords[1] - 1: -1;
        int topWhite = whiteKingCoords[0] > 0 ? whiteKingCoords[0] - 1: -1;
        int bottomWhite = whiteKingCoords[0] < board.length ? whiteKingCoords[0] + 1: board.length;
        int rightWhite = whiteKingCoords[1] < board.length ? whiteKingCoords[1] + 1: board.length;
        int leftWhite = whiteKingCoords[1] > 0 ? whiteKingCoords[1] - 1: -1;
        //counter for how many spots are unreachable
        int voidCount = 0;
        //counter for valud positions
        int validPositions = 0;
        //counter for how many positions are actaully able to be gotten
        int positionGotten = 0;
        //for the black side
        if ((int)side==(int)'b') {
            //Loop through all the spots around the king
            for (int i=topBlack; i<topBlack+3; i++) {
                for (int e=leftBlack; e<leftBlack+3; e++) {
                    //if the spots are literally unreachable in theory increase the counter
                    if (i<0 || e<0 || i>=board.length || e>=board[0].length) { voidCount++; }
                    //if the pieces are able to be gotten to and aren't taken up by like other peices of the same color then increase that counter
                    if (i>=0 && e>=0 && i<board.length && e<board[0].length) {
                        if ((int)board[i][e].charAt(0)==(int)'b') { voidCount++; }
                        else { validPositions++; }
                    }
                    //loop through all the peices on the entire board and if they are like valid peices to move(not the king) try to move them to a area around the king
                    for (int row=0; row<board.length; row++) {
                        for (int column=0; column<board[0].length; column++) {
                            //Make sure the peice is vaid and isn't the king
                            if ((i>=0 && e>=0 && i<board.length && e<board[0].length) && !(i==topBlack+1 && e==leftBlack+1)) {
                                if ((int)board[row][column].charAt(0)!=(int)'-') {
                                    //makes sure the peice being moved is not empty and the spot its going to is not black, because that a void spot
                                    if ((int)board[i][e].charAt(0)!=(int)'b') {
                                        //Goes through all the peices depending on what they are and trying to move them to the position around the king
                                        if ((int)(board[row][column]).charAt(1)==(int)'K' && (int)(board[row][column]).charAt(0)!=(int)'b') {
                                            String[][] newBoard = copyArray(board);
                                            king(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e], 1, 1);
                                            //If it works and the peice is able to get there plus its a valid spot that needs to be covered then increase counter
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                        //Other statemates follow the same login as ^
                                        else if ((int)(board[row][column]).charAt(1)==(int)'Q') {
                                            String[][] newBoard = copyArray(board);
                                            queen(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e]);
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                        else if ((int)(board[row][column]).charAt(1)==(int)'B') {
                                            String[][] newBoard = copyArray(board);
                                            bishop(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e]);
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                        else if ((int)(board[row][column]).charAt(1)==(int)'H') {
                                            String[][] newBoard = copyArray(board);
                                            knight(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e]);
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                        else if ((int)(board[row][column]).charAt(1)==(int)'R') {
                                            String[][] newBoard = copyArray(board);
                                            rook(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e], 1);
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                        else if ((int)(board[row][column]).charAt(1)==(int)'P') {
                                            String[][] newBoard = copyArray(board);
                                            pawn(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e]);
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        //For the other side same logic as black just opposite side so some of the things will be swapped but otherwise the same
        else if ((int)side==(int)'w') {
            for (int i=topWhite; i<topWhite+3; i++) {
                for (int e=leftWhite; e<leftWhite+3; e++) {
                    if (i<0 || e<0 || i>=board.length || e>=board[0].length) { voidCount++; }
                    if (i>=0 && e>=0 && i<board.length && e<board[0].length) {
                        if ((int)board[i][e].charAt(0)==(int)'w') { voidCount++; }
                        else { validPositions++; }
                    }
                    for (int row=0; row<board.length; row++) {
                        for (int column=0; column<board[0].length; column++) {
                            if ((i>=0 && e>=0 && i<board.length && e<board[0].length) && !(i==topWhite+1 && e==leftWhite+1)) {
                                if ((int)board[row][column].charAt(0)!=(int)'-') {
                                    if ((int)board[i][e].charAt(0)!=(int)'w') {
                                        if ((int)(board[row][column]).charAt(1)==(int)'K' && (int)(board[row][column]).charAt(0)!=(int)'w') {
                                            String[][] newBoard = copyArray(board);
                                            king(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e], 1, 1);
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                        else if ((int)(board[row][column]).charAt(1)==(int)'Q') {
                                            String[][] newBoard = copyArray(board);
                                            queen(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e]);
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                        else if ((int)(board[row][column]).charAt(1)==(int)'B') {
                                            String[][] newBoard = copyArray(board);
                                            bishop(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e]);
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                        else if ((int)(board[row][column]).charAt(1)==(int)'H') {
                                            String[][] newBoard = copyArray(board);
                                            knight(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e]);
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                        else if ((int)(board[row][column]).charAt(1)==(int)'R') {
                                            String[][] newBoard = copyArray(board);
                                            rook(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e], 1);
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                        else if ((int)(board[row][column]).charAt(1)==(int)'P') {
                                            String[][] newBoard = copyArray(board);
                                            pawn(newBoard, coordBoard, coordBoard[row][column], coordBoard[i][e]);
                                            if (!compareArrays(board, newBoard)) { positionGotten++; }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        //If there are no positons that are valud then stalemate is not possible
        if (voidCount==9) {
            return false;
        }
        //if all the valiud positions are gotten and there are more than 0 valid positions then stalemate
        else if (validPositions==positionGotten && validPositions!=0) {
            return true;
        }
        //anything else results in not a stalemate
        return false;
    }
	public static void main(String[] args) {
        //Set up scanner for user input on positions and stuff
		Scanner r = new Scanner(System.in);
        //Set up the chess board peices and coordinate system
		String[][] chessPieces = {{"bR", "bH", "bB", "bQ", "bK", "bB", "bH", "bR"}, {"bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"}, {"-", "-", "-", "-", "-", "-", "-", "-"}, {"-", "-", "-", "-", "-", "-", "-", "-"}, {"-", "-", "-", "-", "-", "-", "-", "-"}, {"-", "-", "-", "-", "-", "-", "-", "-"}, {"wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"}, {"wR", "wH", "wB", "wQ", "wK", "wB", "wH", "wR"}};
		String[][] chessBoardCoordinates = {{"a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"}, {"a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"}, {"a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"}, {"a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"}, {"a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"}, {"a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"}, {"a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"},{"a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"}};
        //Staring variables to count king and rook moves as well as record what the coords of a peice are when the user refers to it
		boolean gameActive = true; int bKingMoves = 0; int bRookMoves = 0;
        int wKingMoves = 0; int wRookMoves = 0;
		int[] piece = new int[2];
        boolean player1 = true; boolean player2 = true;
        //Copy the board as a comparison to one that will be changing each turn
		String[][] newBoard = copyArray(chessPieces);
        //Set up strings that will be used by user to get position and where they want to go
		String position; String proposedCoord;
		System.out.println("Welcome to Chess");
        //Print out the board
		printBoard(chessPieces);
        //Loops will the game is active, will end with stalemate or checkmate
		while (gameActive) {
			while (player1) {
                //Gets information on what player 1 wants to do with their turn
				System.out.println("Player 1, Enter Coordinate of piece to move and coordinate of where you want to move that peice to");
				System.out.print("Piece coords: ");
				position = r.nextLine();
				System.out.print("To: ");
				proposedCoord = r.nextLine();
				piece = convert(chessBoardCoordinates, position);
                //Runs if the user puts in the starting coords as the other team or a empty place and gets new coords
				while ((int)chessPieces[piece[0]][piece[1]].charAt(0)==(int)'-' || (int)chessPieces[piece[0]][piece[1]].charAt(0)==(int)'b') {
                    System.out.println("Wrong piece or empty square: ");
					System.out.print("Piece coords: ");
					position = r.nextLine();
					System.out.print("To: ");
					proposedCoord = r.nextLine();
					piece = convert(chessBoardCoordinates, position);
				}
                //Depending on what peice they chose to move, choose the correct method and plug in where they are and where they want to be
				switch (chessPieces[piece[0]][piece[1]].charAt(1)) {
					case 'P':
						pawn(chessPieces, chessBoardCoordinates, position, proposedCoord);
						break;
					case 'R':
						rook(chessPieces, chessBoardCoordinates, position, proposedCoord, wRookMoves);
						break;
					case 'H':
						knight(chessPieces, chessBoardCoordinates, position, proposedCoord);
						break;
					case 'B':
						bishop(chessPieces, chessBoardCoordinates, position, proposedCoord);
						break;
					case 'Q':
						queen(chessPieces, chessBoardCoordinates, position, proposedCoord);
						break;
					case 'K':
						king(chessPieces, chessBoardCoordinates, position, proposedCoord, wKingMoves, wRookMoves);
						break;
				}
                //Makes sure that that the player made and move and it doesn't put them in check
                if (!compareArrays(chessPieces, newBoard) && !check(chessPieces, chessBoardCoordinates, 'w')) {
                    break;
                }
                //If the player is in check, this resets their move so they can't move two pieces at once
                else if (check(chessPieces, chessBoardCoordinates, 'w')) {
                    System.out.println("Still in check");
                    //Get new spot that falsly moved peice is in
                    piece = convert(chessBoardCoordinates, proposedCoord);
                    //Depnding on what peice it is, move it back by reversing parameters
                    switch (chessPieces[piece[0]][piece[1]].charAt(1)) {
                        case 'P':
                            pawn(chessPieces, chessBoardCoordinates, proposedCoord, position);
                            break;
                        case 'R':
                            rook(chessPieces, chessBoardCoordinates, proposedCoord, position, wRookMoves);
                            wRookMoves-=2;
                            break;
                        case 'H':
                            knight(chessPieces, chessBoardCoordinates, proposedCoord, position);
                            break;
                        case 'B':
                            bishop(chessPieces, chessBoardCoordinates, proposedCoord, position);
                            break;
                        case 'Q':
                            queen(chessPieces, chessBoardCoordinates, proposedCoord, position);
                            break;
                        case 'K':
                            king(chessPieces, chessBoardCoordinates, proposedCoord, position, wKingMoves, wRookMoves);
                            wKingMoves-=2;
                            break;
                    }
                }
                //let user know they are doing something wrong
                else { System.out.println("Move invalid"); }
			}
            //Checkmate if stalemate and check at the same time, but does the same thing as stalemate stuff below
            if (stalemate(chessPieces, chessBoardCoordinates, 'b') && check(chessPieces, chessBoardCoordinates, 'b')) { //checkmate
                gameActive = false;
                break;
            }
            //Ends game at a white stalemate, ends loop and makes sure it can't come back
            else if (stalemate(chessPieces, chessBoardCoordinates, 'w')) {
                gameActive = false;
                break;
            }
            //Ends the game since black stalemate and makes sure loop can't come back
            else if (stalemate(chessPieces, chessBoardCoordinates, 'b')) {
                gameActive = false;
                break;
            }
            //Lets the player know that they are in check
            else if (check(chessPieces, chessBoardCoordinates, 'b')) {
                System.out.println("Black is in check");
            }
            System.out.print("\033[H\033[2J");
            System.out.flush();
            //creates a copy of the playing board and variables to loop through the board
            newBoard = copyArray(chessPieces);
            printBoard(chessPieces);
			while (player2) {
                //Gather what player 2 wants to do for their move
				System.out.println("Player 2, Enter Coordinate of piece to move and coordinate of where you want to move that peice to");
				System.out.print("Piece coords: ");
				position = r.nextLine();
				System.out.print("To: ");
				proposedCoord = r.nextLine();
                //convert the standard chess coordinates to numerical array values for use in methods
				piece = convert(chessBoardCoordinates, position);
                //if the selected peice is the wrong team or an empty space ask them for a different input
				while ((int)chessPieces[piece[0]][piece[1]].charAt(0)==(int)'-' || (int)chessPieces[piece[0]][piece[1]].charAt(0)==(int)'w') {
					System.out.println("Wrong piece or empty square: ");
					System.out.print("Piece coords: ");
					position = r.nextLine();
					System.out.print("To: ");
					proposedCoord = r.nextLine();
					piece = convert(chessBoardCoordinates, position);
				}
                //Given which chess peices they selected to move, plug in the coordinates they want to move to and which peice they want to move into the correct method
				switch (chessPieces[piece[0]][piece[1]].charAt(1)) {
					case 'P':
						pawn(chessPieces, chessBoardCoordinates, position, proposedCoord);
						break;
					case 'R':
						rook(chessPieces, chessBoardCoordinates, position, proposedCoord, bRookMoves);
						break;
					case 'H':
						knight(chessPieces, chessBoardCoordinates, position, proposedCoord);
						break;
					case 'B':
						bishop(chessPieces, chessBoardCoordinates, position, proposedCoord);
						break;
					case 'Q':
						queen(chessPieces, chessBoardCoordinates, position, proposedCoord);
						break;
					case 'K':
						king(chessPieces, chessBoardCoordinates, position, proposedCoord, bKingMoves, bRookMoves);
						break;
				}
                //Make sure the player can't come a player into a position where they are either in check or checkmate
                if (!compareArrays(chessPieces, newBoard) && !check(chessPieces, chessBoardCoordinates, 'b')) {
                    break;
                }
                //If the player is in check, this resets their move so they can't move two pieces at once
                else if (check(chessPieces, chessBoardCoordinates, 'b')) {
                    System.out.println("Still in check");
                    //resets peices to address the new position of the pice
                    piece = convert(chessBoardCoordinates, proposedCoord);
                    //depending on what the peice is choose the approp method but with position and where it wants to go reversed to move it back
                    switch (chessPieces[piece[0]][piece[1]].charAt(1)) {
                        case 'P':
                            pawn(chessPieces, chessBoardCoordinates, proposedCoord, position);
                            break;
                        case 'R':
                            rook(chessPieces, chessBoardCoordinates, proposedCoord, position, bRookMoves);
                            //Reset rook moves to where it would have been
                            bRookMoves-=2;
                            break;
                        case 'H':
                            knight(chessPieces, chessBoardCoordinates, proposedCoord, position);
                            break;
                        case 'B':
                            bishop(chessPieces, chessBoardCoordinates, proposedCoord, position);
                            break;
                        case 'Q':
                            queen(chessPieces, chessBoardCoordinates, proposedCoord, position);
                            break;
                        case 'K':
                            king(chessPieces, chessBoardCoordinates, proposedCoord, position, bKingMoves, bRookMoves);
                            //reset king moves to where it would have been
                            bKingMoves-=2;
                            break;
                    }
                }
                //let user know they are doing something wrong
                else { System.out.println("Move invalid"); }
			}
            //checkmate if true, breaks if true and makes sure loop can't come back
            if (stalemate(chessPieces, chessBoardCoordinates, 'w') && check(chessPieces, chessBoardCoordinates, 'w')) {
                gameActive = false;
                break;
            }
            //checks if there is a stalemate and break the loop and make sure it can't come back
            else if (stalemate(chessPieces, chessBoardCoordinates, 'b')) {
                gameActive = false;
                break;
            }
            else if (stalemate(chessPieces, chessBoardCoordinates, 'w')) {
                gameActive = false;
                break;
            }
            //Check if the white piece is in check and print something if it is
            else if (check(chessPieces, chessBoardCoordinates, 'w')) {
                System.out.println("White is in check");
            }
            System.out.print("\033[H\033[2J");
            System.out.flush();
            //creates a copy of the playing board and variables to loop through the board
            newBoard = copyArray(chessPieces);
			printBoard(chessPieces);
            //if there is a stalemate and check then that means checkmate so end the game and display who wins for each color
            if (stalemate(chessPieces, chessBoardCoordinates, 'w') && check(chessPieces, chessBoardCoordinates, 'w')) {
                System.out.println("\nBlack wins!");
            }
            else if (stalemate(chessPieces, chessBoardCoordinates, 'b') && check(chessPieces, chessBoardCoordinates, 'b')) {
                System.out.println("\nWhite wins!");
            }
            //if statemate of either color, just rechecks so another variable doesn't need to get created
            else if (stalemate(chessPieces, chessBoardCoordinates, 'w')) {
                System.out.println("\nWhite stalemate");
            }
            else if (stalemate(chessPieces, chessBoardCoordinates, 'b')) {
                System.out.println("\nWhite stalemate");
            }
        }
	}
}
