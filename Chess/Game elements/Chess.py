from tkinter import *
from tkinter.messagebox import showinfo

import numpy as np
from PIL import ImageTk, Image


class every_piece:
    def __init__(self,location,image,color,order):
        self.order = order
        self.first_move = True
        self.location = location
        self.color = color
        self.bg_color = "#6E6A5C" if np.sum(self.location) % 2 else "#F3DD8B"
        self.other_team = chess.whites if color == "black" else chess.blacks
        self.image = self.image_arrange(image)
        self.label = None
        self.create()
        self.is_clicked = False
    def legal_moves(self):
        chess.piece_calculator()
        king = chess.bk if self.color == "black" else chess.wk
        p = self.possible()
        possible = p.copy()
        if self.color == "black":
            chess.turn = "white"
            for j in range(len(chess.white_pieces)):
                for i in p:
                    chess.chess_board[self.location[0], self.location[1]] = 0
                    current_location = self.location
                    self.location = i
                    code_of_the_box = chess.chess_board[i[0], i[1]]
                    chess.chess_board[i[0], i[1]] = self.type
                    skip = king.location in chess.white_pieces[j].possible()
                    if chess.white_pieces[j].location == i:
                        skip = False
                    chess.chess_board[i[0], i[1]] = code_of_the_box
                    self.location = current_location
                    chess.chess_board[self.location[0], self.location[1]] = self.type
                    if skip:
                        if i in possible:
                            possible.remove(i)
            chess.turn = "black"
        else:
            chess.turn = "black"
            for j in range(len(chess.black_pieces)):
                for i in p:
                    chess.chess_board[self.location[0], self.location[1]] = 0
                    current_location = self.location
                    self.location = i
                    code_of_the_box = chess.chess_board[i[0], i[1]]
                    chess.chess_board[i[0], i[1]] = self.type
                    skip = king.location in chess.black_pieces[j].possible()
                    if chess.black_pieces[j].location == i:
                        skip = False
                    chess.chess_board[i[0], i[1]] = code_of_the_box
                    self.location = current_location
                    chess.chess_board[self.location[0], self.location[1]] = self.type
                    if skip:
                        if i in possible:
                            possible.remove(i)
            chess.turn = "white"

        chess.turn = "black" if self.color == "black" else "white"
        return possible
    def after_check_designer(self,king,color):
            king.label.destroy()
            frame = Frame(chess.main_frame, bg=color, highlightbackground="black", highlightthickness=0.5)
            frame.place(relwidth=1 / 8, relheight=1 / 8, rely=king.location[0] * 0.125,relx=king.location[1] * 0.125)
            king.create()
            king.label.config(bg=color)
    def en_passant_move(self, event, location):
        epl = chess.en_passant_pawn.location
        ept = chess.en_passant_pawn.type
        chess.chess_board[epl[0]][epl[1]] = 0
        chess.all_pieces[ept//100-1][(ept//10)%10][ept%10] = None
        chess.en_passant_pawn.label.destroy()
        self.move(event,location)
    def image_arrange(self,image):
        img = Image.open(image)
        img = img.resize((70,70), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        return img
    def create(self):
        self.label = Label(chess.main_frame, image=self.image, bg=self.bg_color,cursor= "hand2")
        self.label.bind("<Button-1>", self.click)
        self.label.place(relwidth=1/8-0.01,relheight=1/8-0.01,rely=self.location[0]*0.125+0.005,relx=self.location[1]*0.125+0.005)
    def bg_designer(self):
        self.bg_color = "#6E6A5C" if np.sum(self.location) % 2 else "#F3DD8B"
    def is_castling_possible(self):
        if self.first_move:
            chess.piece_calculator()
            if self.type == 100 and not chess.check_for_black:
                chess.short_castling_w = False
                chess.long_castling_w = False
                if chess.all_pieces[0][4][0] != None:
                    if chess.all_pieces[0][4][0].first_move:
                        if chess.chess_board[0, 6] == 0 and chess.chess_board[0, 5] == 0:
                            chess.turn = "white"
                            k = [j for i in chess.white_pieces for j in i.possible()]
                            chess.turn = "black"
                            if [0, 6] not in k and [0, 5] not in k:
                                if str(chess.chess_board[1, 7])[:2] != "25" and str(chess.chess_board[1, 4])[:2] != "25":
                                    chess.short_castling_b = True
                                else: chess.short_castling_b = False
                            else: chess.short_castling_b = False
                        else: chess.short_castling_b = False
                    else: chess.short_castling_b = False
                else: chess.short_castling_b = False
                if chess.all_pieces[0][4][1] != None:
                    if chess.all_pieces[0][4][1].first_move:
                        if chess.chess_board[0, 2] == 0 and chess.chess_board[0, 3] == 0:
                            chess.turn = "white"
                            k = [j for i in chess.white_pieces for j in i.possible()]
                            chess.turn = "black"
                            if [0, 2] not in k and [0, 3] not in k:
                                if str(chess.chess_board[1, 1])[:2] != "25":
                                    chess.long_castling_b = True
                                else: chess.long_castling_b = False
                            else: chess.long_castling_b = False
                        else: chess.long_castling_b = False
                    else: chess.long_castling_b = False
                else: chess.long_castling_b = False
            elif self.type == 200 and not chess.check_for_white:
                chess.short_castling_b = False
                chess.long_castling_b = False
                if chess.all_pieces[1][4][0] != None:
                    if chess.all_pieces[1][4][0].first_move:
                        if chess.chess_board[7, 6] == 0 and chess.chess_board[7, 5] == 0:
                            chess.turn = "black"
                            k = [j for i in chess.black_pieces for j in i.possible()]
                            chess.turn = "white"
                            if [7, 6] not in k and [7, 5] not in k:
                                if str(chess.chess_board[6, 7])[:2] != "15" and str(chess.chess_board[6, 4])[:2] != "15":
                                    chess.short_castling_w = True
                                else: chess.short_castling_w = False
                            else: chess.short_castling_w = False
                        else: chess.short_castling_w = False
                    else: chess.short_castling_w = False
                else: chess.short_castling_w = False
                if chess.all_pieces[1][4][1] != None:
                    if chess.all_pieces[1][4][1].first_move:
                        if chess.chess_board[7, 2] == 0 and chess.chess_board[7, 3] == 0:
                            chess.turn = "black"
                            k = [j for i in chess.black_pieces for j in i.possible()]
                            chess.turn = "white"
                            if [7, 2] not in k and [7, 3] not in k:
                                if str(chess.chess_board[6, 1])[:2] != "15":
                                    chess.long_castling_w = True
                                else: chess.long_castling_w = False
                            else: chess.long_castling_w = False
                        else: chess.long_castling_w = False
                    else: chess.long_castling_w = False
                else: chess.long_castling_w = False
            else:
                chess.short_castling_w = False
                chess.long_castling_w = False
                chess.short_castling_b = False
                chess.long_castling_b = False
        else:
            chess.short_castling_w = False
            chess.long_castling_w = False
            chess.short_castling_b = False
            chess.long_castling_b = False
    def promote_to_queen(self,image,frame):
        chess.queen_creator(self.location, image, self.color)
        chess.all_pieces[self.type//100-1][5][self.type%10] = None
        chess.promoting = False
        frame.destroy()
    def promote_to_rook(self,image,frame):
        chess.rook_creator(self.location, image, self.color)
        chess.all_pieces[self.type // 100 - 1][5][self.type % 10] = None
        chess.promoting = False
        frame.destroy()
    def promote_to_bishop(self,image,frame):
        chess.bishop_creator(self.location, image, self.color)
        chess.all_pieces[self.type // 100 - 1][5][self.type % 10] = None
        chess.promoting = False
        frame.destroy()
    def promote_to_knight(self,image,frame):
        chess.knight_creator(self.location, image, self.color)
        chess.all_pieces[self.type // 100 - 1][5][self.type % 10] = None
        chess.promoting = False
        frame.destroy()
    def main_promote(self):
        if self.type // 10 == 15 and self.location[0] == 7:
            chess.promoting = True
            self.bg_designer()
            frame = Frame(chess.main_frame, bg=self.bg_color, highlightbackground="black", highlightthickness=0.5)
            frame.place(relwidth=1 / 8, relheight=1 / 8, rely=self.location[0] * 0.125, relx=self.location[1] * 0.125)
            frame = Frame(chess.main_frame,bg="white",highlightbackground="black",highlightthickness=0.5)
            frame.place(relheight=1/4,relwidth=9/16,relx=7/32,rely=13/32)
            label0 = Label(frame,bg="white",text="PROMOTE",font="Arial 18 bold")
            img1 = "queen_b.png"
            label1 = Label(frame,image=queen_img_b,bg="white",cursor="hand2")
            img2 = "rook_b.png"
            label2 = Label(frame,image=rook_img_b,bg="white",cursor="hand2")
            img3 = "knight_b.png"
            label3 = Label(frame,image=knight_img_b,bg="white",cursor="hand2")
            img4 = "bishop_b.png"
            label4 = Label(frame,image=bishop_img_b, bg="white",cursor="hand2")
            label0.pack(side=TOP)
            label1.place(relwidth=2/9,relheight=1/2,rely=3/8,relx=1/18)
            label2.place(relwidth=2/9,relheight=1/2,rely=3/8,relx=5/18)
            label3.place(relwidth=2/9,relheight=1/2,rely=3/8,relx=9/18)
            label4.place(relwidth=2/9,relheight=1/2,rely=3/8,relx=13/18)
        elif self.type // 10 == 25 and self.location[0] == 0:
            chess.promoting = True
            self.bg_designer()
            frame = Frame(chess.main_frame, bg=self.bg_color, highlightbackground="black", highlightthickness=0.5)
            frame.place(relwidth=1 / 8, relheight=1 / 8, rely=self.location[0] * 0.125, relx=self.location[1] * 0.125)
            frame = Frame(chess.main_frame, bg="white", highlightbackground="black", highlightthickness=0.5)
            frame.place(relheight=1 / 4, relwidth=9 / 16, relx=7 / 32, rely=13 / 32)
            label0 = Label(frame, bg="white", text="PROMOTE", font="Arial 18 bold")
            img1 = "queen_w.png"
            label1 = Label(frame, image=queen_img_w, bg="white",cursor="hand2")
            img2 = "rook_w.png"
            label2 = Label(frame, image=rook_img_w, bg="white",cursor="hand2")
            img3 = "knight_w.png"
            label3 = Label(frame, image=knight_img_w, bg="white",cursor="hand2")
            img4 = "bishop_w.png"
            label4 = Label(frame, image=bishop_img_w, bg="white",cursor="hand2")
            label0.pack(side=TOP)
            label1.place(relwidth=2 / 9, relheight=1 / 2, rely=3 / 8, relx=1 / 18)
            label2.place(relwidth=2 / 9, relheight=1 / 2, rely=3 / 8, relx=5 / 18)
            label3.place(relwidth=2 / 9, relheight=1 / 2, rely=3 / 8, relx=9 / 18)
            label4.place(relwidth=2 / 9, relheight=1 / 2, rely=3 / 8, relx=13 / 18)
        if (self.type // 10 == 15 and self.location[0] == 7) or (self.type // 10 == 25 and self.location[0] == 0):
            label1.bind("<Button-1>",lambda event,image=img1,frame = frame: self.promote_to_queen(image,frame))
            label2.bind("<Button-1>",lambda event,image=img2,frame = frame: self.promote_to_rook(image,frame))
            label3.bind("<Button-1>",lambda event,image=img3,frame = frame: self.promote_to_knight(image,frame))
            label4.bind("<Button-1>",lambda event,image=img4,frame = frame: self.promote_to_bishop(image,frame))
    def move(self,event,location):
        if self.color == "black":
            if chess.check_for_black:
                self.after_check_designer(chess.bk,chess.bk.bg_color)
                chess.check_for_black = False
        else:
            if chess.check_for_white:
                self.after_check_designer(chess.wk, chess.wk.bg_color)
                chess.check_for_white = False
        if location in self.squares_with_enemy:
            a = chess.chess_board[location[0],location[1]]
            color,type,order = list(map(int,list(str(a))))
            chess.all_pieces[color-1][type][order] = None
            chess.piece_calculator()
        if self.first_move:
            self.first_move = False
        if abs(self.location[0]-location[0]) == 2 and (self.type//10)%10 == 5:
            chess.en_passant = True
            chess.en_passant_pawn = chess.all_pieces[self.type//100-1][5][self.type%10]
        else:
            chess.en_passant = False
            chess.en_passant_pawn = None
        chess.chess_board[self.location[0], self.location[1]] = 0
        self.location = location
        chess.chess_board[self.location[0], self.location[1]] = self.type
        self.bg_designer()
        self.label.destroy()
        for i in self.boxes:
            if i == None:
                break
            i[0].destroy()

        frame = Frame(chess.main_frame, bg=self.bg_color,highlightbackground="black",highlightthickness=0.5)
        frame.place(relwidth=1 / 8, relheight=1 / 8, rely=self.location[0] * 0.125,relx=self.location[1] * 0.125)
        self.create()
        other_king = chess.wk if self.color == "black" else chess.bk
        chess.piece_calculator()
        if self.color == "black":
            if other_king.location in [j for i in chess.black_pieces for j in i.legal_moves()]:
                chess.check_for_white = True
                self.after_check_designer(other_king,"red")
        else:
            if other_king.location in [j for i in chess.white_pieces for j in i.legal_moves()]:
                chess.check_for_black = True
                self.after_check_designer(other_king, "red")


        if len([j for i in chess.black_pieces for j in i.legal_moves()]) == 0:
            not_move = len([j for i in chess.black_pieces for j in i.legal_moves()])
            if chess.check_for_black and not_move == 0:
                showinfo("CHECKMATE!","White Wins!")
            elif not chess.check_for_black and not not_move:
                showinfo("Stalemate!","Tie!")
        elif len([j for i in chess.white_pieces for j in i.legal_moves()]) == 0:
            not_move = len([j for i in chess.white_pieces for j in i.legal_moves()])
            if chess.check_for_white and not_move == 0:
                showinfo("CHECKMATE!","Black Wins!")
            elif not chess.check_for_white and not not_move:
                showinfo("Stalemate!","Tie!")
        chess.is_clicked = False
        chess.turn = "white" if self.color == "black" else "black"
        self.main_promote()
    def click(self,label):
        if chess.turn != self.color or chess.promoting:
            return
        self.possible_squares = self.legal_moves()
        if chess.is_clicked:
            a = chess.currently_clicked
            chess.is_clicked = False
            chess.currently_clicked = None
            if not self.is_clicked:
                a.click("")
        if not self.is_clicked:
            chess.is_clicked = True
            self.is_clicked = True
            boxes = self.possible_squares.copy()
            self.is_castling_possible()
            while len(boxes) != 28:
                boxes.append(None)
            self.boxes = boxes
            for index,value in enumerate(self.boxes):
                if value == None:
                    break
                color = "#6E6A5C" if np.sum(value) % 2 else "#F3DD8B"
                if value in self.squares_with_enemy:
                    color = "red"
                value = Label(chess.main_frame,image=chess.square,cursor="hand2",bg=color)
                value.place(relwidth=1 / 16, relheight=1 / 16, rely=self.boxes[index][0] * 0.125+1/32, relx=self.boxes[index][1] * 0.125+1/32)
                self.boxes[index] = [value,self.boxes[index]]
            if chess.long_castling_b:
                color = "#F3DD8B"
                value = Label(chess.main_frame, image=chess.square, cursor="hand2", bg=color)
                value.place(relwidth=1 / 16, relheight=1 / 16, rely=1 / 32,relx=2 * 0.125 + 1 / 32)
                self.boxes.insert(0,[value,[0,2]])
            if chess.long_castling_w:
                color = "#6E6A5C"
                value = Label(chess.main_frame, image=chess.square, cursor="hand2", bg=color)
                value.place(relwidth=1 / 16, relheight=1 / 16, rely=7 * 0.125 + 1 / 32,relx=2 * 0.125 + 1 / 32)
                self.boxes.insert(0,[value,[7,2]])
            if chess.short_castling_b:
                color = "#F3DD8B"
                value = Label(chess.main_frame, image=chess.square, cursor="hand2", bg=color)
                value.place(relwidth=1 / 16, relheight=1 / 16, rely=1 / 32,relx=6 * 0.125 + 1 / 32)
                self.boxes.insert(0,[value,[0,6]])
            if chess.short_castling_w:
                color = "#6E6A5C"
                value = Label(chess.main_frame, image=chess.square, cursor="hand2", bg=color)
                value.place(relwidth=1 / 16, relheight=1 / 16, rely=7 * 0.125 + 1 / 32,relx=6 * 0.125 + 1 / 32)
                self.boxes.insert(0,[value,[7,6]])

            chess.currently_clicked = chess.all_pieces[self.type//100-1][(self.type//10)%10][self.type%10]
            sw = chess.short_castling_w
            sb = chess.short_castling_b
            lw = chess.long_castling_w
            lb = chess.long_castling_b
            for i in self.boxes:
                if i == None:
                    break
                i[0].bind("<Button-1>", lambda event ,location = i[1]:self.move(event,location))
                if chess.long_castling_b and i[1] == [0,2]:
                    i[0].bind("<Button-1>", lambda event ,location = i[1],king = chess.bk : chess.castle(event,location,king))
                if chess.long_castling_w and i[1] == [7,2]:
                    i[0].bind("<Button-1>", lambda event ,location = i[1],king = chess.wk : chess.castle(event,location,king))
                if chess.short_castling_b and i[1] == [0,6]:
                    chess.short_castling_b = False
                    i[0].bind("<Button-1>", lambda event ,location = i[1],king = chess.bk : chess.castle(event,location,king))
                if chess.short_castling_w and i[1] == [7,6]:
                    chess.short_castling_w = False
                    i[0].bind("<Button-1>", lambda event ,location = i[1],king = chess.wk : chess.castle(event,location,king))

            chess.short_castling_w = sw
            chess.short_castling_b = sb
            chess.long_castling_w = lw
            chess.long_castling_b = lb

            if chess.en_passant:
                if self.color == "black":
                    for i in [[0,-1],[0,1]]:
                        try:
                            [self.location[0]+i[0],self.location[1]+i[1]]
                        except:
                            continue
                        if chess.en_passant_pawn.location == [self.location[0]+i[0],self.location[1]+i[1]]:
                            location = [self.location[0]+1,self.location[1]+i[1]]
                            value = Label(chess.main_frame, image=chess.square, cursor="hand2", bg="red")
                            value.place(relwidth=1 / 16, relheight=1 / 16,rely=location[0] * 0.125+1/32, relx=location[1] * 0.125+1/32)
                            value.bind("<Button-1>",lambda event, location=location:self.en_passant_move(event,location))
                            self.boxes.insert(0,[value,location])
                else:
                    for i in [[0,-1],[0,1]]:
                        try:
                            [self.location[0]+i[0],self.location[1]+i[1]]
                        except:
                            continue
                        if chess.en_passant_pawn.location == [self.location[0]+i[0],self.location[1]+i[1]]:
                            location = [self.location[0]-1,self.location[1]+i[1]]
                            value = Label(chess.main_frame, image=chess.square, cursor="hand2", bg="red")
                            value.place(relwidth=1 / 16, relheight=1 / 16, rely=location[0] * 0.125+1/32, relx=location[1] * 0.125+1/32)
                            value.bind("<Button-1>",lambda event, location=location:self.en_passant_move(event,location))
                            self.boxes.insert(0, [value, location])
        else:
            self.is_clicked = False
            for i in self.boxes:
                if i == None:
                    break
                i[0].destroy()
class queen(every_piece):
    def __init__(self,location,image,color,order):
        super().__init__(location,image,color,order)
        self.type = 11*10+self.order if self.color == "black" else 21*10+self.order
        chess.chess_board[self.location[0], self.location[1]] = self.type
        self.possible_squares = self.possible()
    def possible(self):
        possible = []
        self.squares_with_enemy = []
        if chess.turn != self.color:
            return possible
        for i in range(1,8-self.location[1]):
            if chess.chess_board[self.location[0],self.location[1]+i] == 0:
                possible.append([self.location[0],self.location[1]+i])
            elif int(str(chess.chess_board[self.location[0],self.location[1]+i])[:2]) in self.other_team:
                possible.append([self.location[0], self.location[1] + i])
                self.squares_with_enemy.append([self.location[0], self.location[1] + i])
                break
            else:
                break
        for i in range(1,self.location[1]+1):
            if chess.chess_board[self.location[0],self.location[1]-i] == 0:
                possible.append([self.location[0],self.location[1]-i])
            elif int(str(chess.chess_board[self.location[0],self.location[1]-i])[:2]) in self.other_team:
                possible.append([self.location[0], self.location[1] - i])
                self.squares_with_enemy.append([self.location[0], self.location[1] - i])
                break
            else:
                break
        for j in range(1,8-self.location[0]):
            if chess.chess_board[self.location[0]+j,self.location[1]] == 0:
                possible.append([self.location[0]+j,self.location[1]])
            elif int(str(chess.chess_board[self.location[0]+j,self.location[1]])[:2]) in self.other_team:
                possible.append([self.location[0]+j, self.location[1]])
                self.squares_with_enemy.append([self.location[0]+j, self.location[1]])
                break
            else:
                break
        for j in range(1,self.location[0]+1):
            if chess.chess_board[self.location[0]-j,self.location[1]] == 0:
                possible.append([self.location[0]-j,self.location[1]])
            elif int(str(chess.chess_board[self.location[0]-j,self.location[1]])[:2]) in self.other_team:
                possible.append([self.location[0]-j, self.location[1]])
                self.squares_with_enemy.append([self.location[0]-j, self.location[1]])
                break
            else:
                break
        diagonals = [chess.chess_board[self.location[0]:,self.location[1]:].diagonal(),
                     np.rot90(chess.chess_board[self.location[0]:,:self.location[1]+1]).diagonal(),
                     np.rot90(np.rot90(np.rot90(chess.chess_board[:self.location[0]+1,self.location[1]:]))).diagonal(),
                     np.rot90(np.rot90(chess.chess_board[:self.location[0]+1:,:self.location[1]+1])).diagonal()]
        for index,value in enumerate(diagonals[0]):
            if index == 0:
                continue
            if value == 0:
                possible.append([self.location[0]+ index, self.location[1]+index])
            elif int(str(value)[:2]) in self.other_team:
                possible.append([self.location[0] + index, self.location[1] + index])
                self.squares_with_enemy.append([self.location[0] + index, self.location[1] + index])
                break
            else:
                break
        for index,value in enumerate(diagonals[1]):
            if index == 0:
                continue
            if value == 0:
                possible.append([self.location[0]+ index, self.location[1]-index])
            elif int(str(value)[:2]) in self.other_team:
                possible.append([self.location[0] + index, self.location[1] - index])
                self.squares_with_enemy.append([self.location[0] + index, self.location[1] - index])
                break
            else:
                break
        for index,value in enumerate(diagonals[2]):
            if index == 0:
                continue
            if value == 0:
                possible.append([self.location[0]- index, self.location[1]+index])
            elif int(str(value)[:2])in self.other_team:
                possible.append([self.location[0] - index, self.location[1] + index])
                self.squares_with_enemy.append([self.location[0] - index, self.location[1] + index])
                break
            else:
                break
        for index,value in enumerate(diagonals[3]):
            if index == 0:
                continue
            if value == 0:
                possible.append([self.location[0]- index, self.location[1]-index])
            elif int(str(value)[:2]) in self.other_team:
                possible.append([self.location[0] - index, self.location[1] - index])
                self.squares_with_enemy.append([self.location[0] - index, self.location[1] - index])
                break
            else:
                break

        return possible
class king(every_piece):
    def __init__(self,location,image,color,order):
        super().__init__(location,image,color,order)
        self.type = 10*10+self.order if self.color == "black" else 20*10+self.order
        chess.chess_board[self.location[0],self.location[1]] = self.type
        self.possible_squares = self.possible()
    def possible(self):
        possible = []
        self.squares_with_enemy = []
        if chess.turn != self.color:
            return possible
        for i in range(-1,2):
            for j in range(-1,2):
                try:
                    chess.chess_board[self.location[0] + i, self.location[1] + j]
                except:
                    continue
                if self.location[0]+i < 0 or self.location[1]+j < 0:
                    continue
                if chess.chess_board[self.location[0]+i,self.location[1]+j] == 0:
                    possible.append([self.location[0] + i, self.location[1] + j])
                elif int(str(chess.chess_board[self.location[0]+i,self.location[1]+j])[:2]) in self.other_team :
                    possible.append([self.location[0]+i,self.location[1]+j])
                    self.squares_with_enemy.append([self.location[0]+i,self.location[1]+j])

        return possible
class knight(every_piece):
    def __init__(self,location,image,color,order):
        super().__init__(location,image,color,order)
        self.type = 12*10+self.order if self.color == "black" else 22*10+self.order
        chess.chess_board[self.location[0], self.location[1]] = self.type
        self.possible_squares = self.possible()
    def possible(self):
        possible = []
        self.squares_with_enemy = []
        if chess.turn != self.color:
            return possible
        directions = [[1,2],[-1,2],[1,-2],[-1,-2],[2,1],[-2,1],[2,-1],[-2,-1]]
        for k in directions:
            i = k[0]
            j = k[1]
            try:
                chess.chess_board[self.location[0] + i, self.location[1] + j]
            except:
                continue
            if self.location[0] + i < 0 or self.location[1] + j < 0:
                continue
            if chess.chess_board[self.location[0] + i, self.location[1] + j] == 0:
                possible.append([self.location[0] + i, self.location[1] + j])
            elif int(str(chess.chess_board[self.location[0] + i, self.location[1] + j])[:2]) in self.other_team:
                possible.append([self.location[0] + i, self.location[1] + j])
                self.squares_with_enemy.append([self.location[0] + i, self.location[1] + j])
        return possible
class bishop(every_piece):
    def __init__(self,location,image,color,order):
        super().__init__(location,image,color,order)
        self.type = 13*10+self.order if self.color == "black" else 23*10+self.order
        chess.chess_board[self.location[0], self.location[1]] = self.type
        self.possible_squares = self.possible()
    def possible(self):
        possible = []
        self.squares_with_enemy = []
        if chess.turn != self.color:
            return possible
        diagonals = [chess.chess_board[self.location[0]:, self.location[1]:].diagonal(),
                     np.rot90(chess.chess_board[self.location[0]:, :self.location[1] + 1]).diagonal(),
                     np.rot90(np.rot90(np.rot90(chess.chess_board[:self.location[0] + 1, self.location[1]:]))).diagonal(),
                     np.rot90(np.rot90(chess.chess_board[:self.location[0] + 1:, :self.location[1] + 1])).diagonal()]
        for index, value in enumerate(diagonals[0]):
            if index == 0:
                continue
            if value == 0:
                possible.append([self.location[0] + index, self.location[1] + index])
            elif int(str(value)[:2]) in self.other_team:
                possible.append([self.location[0] + index, self.location[1] + index])
                self.squares_with_enemy.append([self.location[0] + index, self.location[1] + index])
                break
            else:
                break
        for index, value in enumerate(diagonals[1]):
            if index == 0:
                continue
            if value == 0:
                possible.append([self.location[0] + index, self.location[1] - index])
            elif int(str(value)[:2]) in self.other_team:
                possible.append([self.location[0] + index, self.location[1] - index])
                self.squares_with_enemy.append([self.location[0] + index, self.location[1] - index])
                break
            else:
                break
        for index, value in enumerate(diagonals[2]):
            if index == 0:
                continue
            if value == 0:
                possible.append([self.location[0] - index, self.location[1] + index])
            elif int(str(value)[:2]) in self.other_team:
                possible.append([self.location[0] - index, self.location[1] + index])
                self.squares_with_enemy.append([self.location[0] - index, self.location[1] + index])
                break
            else:
                break
        for index, value in enumerate(diagonals[3]):
            if index == 0:
                continue
            if value == 0:
                possible.append([self.location[0] - index, self.location[1] - index])
            elif int(str(value)[:2]) in self.other_team:
                possible.append([self.location[0] - index, self.location[1] - index])
                self.squares_with_enemy.append([self.location[0] - index, self.location[1] - index])
                break
            else:
                break
        return possible
class rook(every_piece):
    def __init__(self,location,image,color,order):
        super().__init__(location,image,color,order)
        self.type = 14*10+self.order if self.color == "black" else 24*10+self.order
        chess.chess_board[self.location[0], self.location[1]] = self.type
        self.possible_squares = self.possible()
    def possible(self):
        possible = []
        self.squares_with_enemy = []
        if chess.turn != self.color:
            return possible
        for i in range(1, 8 - self.location[1]):
            if chess.chess_board[self.location[0], self.location[1] + i] == 0:
                possible.append([self.location[0], self.location[1] + i])
            elif int(str(chess.chess_board[self.location[0], self.location[1] + i])[:2]) in self.other_team:
                possible.append([self.location[0], self.location[1] + i])
                self.squares_with_enemy.append([self.location[0], self.location[1] + i])
                break
            else:
                break
        for i in range(1, self.location[1] + 1):
            if chess.chess_board[self.location[0], self.location[1] - i] == 0:
                possible.append([self.location[0], self.location[1] - i])
            elif int(str(chess.chess_board[self.location[0], self.location[1] - i])[:2]) in self.other_team:
                possible.append([self.location[0], self.location[1] - i])
                self.squares_with_enemy.append([self.location[0], self.location[1] - i])
                break
            else:
                break
        for j in range(1, 8 - self.location[0]):
            if chess.chess_board[self.location[0] + j, self.location[1]] == 0:
                possible.append([self.location[0] + j, self.location[1]])
            elif int(str(chess.chess_board[self.location[0] + j, self.location[1]])[:2]) in self.other_team:
                possible.append([self.location[0] + j, self.location[1]])
                self.squares_with_enemy.append([self.location[0] + j, self.location[1]])
                break
            else:
                break
        for j in range(1, self.location[0] + 1):
            if chess.chess_board[self.location[0] - j, self.location[1]] == 0:
                possible.append([self.location[0] - j, self.location[1]])
            elif int(str(chess.chess_board[self.location[0] - j, self.location[1]])[:2])in self.other_team:
                possible.append([self.location[0] - j, self.location[1]])
                self.squares_with_enemy.append([self.location[0] - j, self.location[1]])
                break
            else:
                break
        return possible
class pawn(every_piece):
    def __init__(self,location,image,color,order):
        super().__init__(location,image,color,order)
        self.type = 15*10+self.order if self.color == "black" else 25*10+self.order
        chess.chess_board[self.location[0], self.location[1]] = self.type
        self.possible_squares = self.possible()
    def possible(self):
        possible = []
        self.squares_with_enemy = []
        if chess.turn != self.color:
            return possible
        if self.color == "white":
            if self.location[0] == 0:
                return possible
            if chess.chess_board[self.location[0]-1,self.location[1]] == 0:
                possible.append([self.location[0]-1,self.location[1]])
                if self.first_move and chess.chess_board[self.location[0]-2,self.location[1]] == 0:
                    possible.append([self.location[0]-2, self.location[1]])
            for i in [-1,1]:
                try:
                    chess.chess_board[self.location[0] - 1 , self.location[1] +i]
                except:
                    continue
                if self.location[1] + i < 0:
                    continue
                if  int(str(chess.chess_board[self.location[0]-1,self.location[1]+i])[:2]) in self.other_team:
                    possible.append([self.location[0]-1, self.location[1] +i])
                    self.squares_with_enemy.append([self.location[0]-1, self.location[1] +i])
        elif self.color == "black":
            if self.location[0] == 7:
                return possible
            if chess.chess_board[self.location[0]+1,self.location[1]] == 0:
                possible.append([self.location[0]+1,self.location[1]])
                if self.first_move and chess.chess_board[self.location[0]+2,self.location[1]] == 0:
                    possible.append([self.location[0]+2, self.location[1]])
            for i in [-1,1]:
                try:
                    chess.chess_board[self.location[0] +1, self.location[1] + i]
                except:
                    continue
                if self.location[1] + i < 0:
                    continue
                if  int(str(chess.chess_board[self.location[0]+1,self.location[1]+i])[:2])in self.other_team:
                    possible.append([self.location[0]+1, self.location[1] + i])
                    self.squares_with_enemy.append([self.location[0]+1, self.location[1] + i])
        return possible
class chess_game:
    def __init__(self):
        self.chess_board = np.zeros((8,8),dtype=int)
        self.blacks = [10,11,12,13,14,15]
        self.whites = [20,21,22,23,24,25]
        self.turn = "white"
        self.en_passant = False
        self.en_passant_pawn = None
        self.check_for_black = False
        self.check_for_white = False
        self.long_castling_b = False
        self.long_castling_w = False
        self.short_castling_b = False
        self.short_castling_w = False
        self.board_creator()
        self.is_clicked = False
        self.promoting = False
        self.currently_clicked = None
        self.number_of_w_king = 0
        self.number_of_w_queen = 0
        self.number_of_w_knight = 0
        self.number_of_w_bishop = 0
        self.number_of_w_rook = 0
        self.number_of_w_pawn = 0
        self.number_of_b_king = 0
        self.number_of_b_queen = 0
        self.number_of_b_knight = 0
        self.number_of_b_bishop = 0
        self.number_of_b_rook = 0
        self.number_of_b_pawn = 0
        self.all_pieces = [[[None],[None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None]],

                           [[None],[None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None]]]
    def all_piece_creator(self):
        self.rook_creator([0,7],"rook_b.png","black")
        self.rook_creator([0,0], "rook_b.png", "black")
        self.rook_creator([7, 7], "rook_w.png", "white")
        self.rook_creator([7, 0], "rook_w.png", "white")
        self.bk = king([0,4],"king_b.png","black",0)
        self.all_pieces[0][0][0] = self.bk
        self.wk = king([7,4],"king_w.png","white",0)
        self.all_pieces[1][0][0] = self.wk
        self.bishop_creator([0,2],"bishop_b.png","black")
        self.bishop_creator([0,5],"bishop_b.png","black")
        self.bishop_creator([7, 2], "bishop_w.png", "white")
        self.bishop_creator([7, 5], "bishop_w.png", "white")
        self.knight_creator([0,1],"knight_b.png","black")
        self.knight_creator([0,6], "knight_b.png", "black")
        self.knight_creator([7, 1], "knight_w.png", "white")
        self.knight_creator([7, 6], "knight_w.png", "white")
        self.queen_creator([0, 3], "queen_b.png", "black")
        self.queen_creator([7, 3], "queen_w.png", "white")
        for j,color in enumerate(["black","white"]):
            for i in range(8):
                image = "pawn_w.png" if j else "pawn_b.png"
                self.pawn_creator([j*5+1,i],image,color)
    def piece_calculator(self):
        self.black_pieces = [j for i in self.all_pieces[0] for j in i if j != None]
        self.white_pieces = [j for i in self.all_pieces[1] for j in i if j != None]
    def queen_creator(self,location,image,color):
        if color == "black":
            q = queen(location,image,color,self.number_of_b_queen)
            self.all_pieces[0][1][self.number_of_b_queen] = q
            self.number_of_b_queen += 1
        else:
            q = queen(location, image, color, self.number_of_w_queen)
            self.all_pieces[1][1][self.number_of_w_queen] = q
            self.number_of_w_queen += 1
    def knight_creator(self,location,image,color):
        if color == "black":
            n = knight(location, image, color, self.number_of_b_knight)
            self.all_pieces[0][2][self.number_of_b_knight] = n
            self.number_of_b_knight += 1
        else:
            n = knight(location, image, color, self.number_of_w_knight)
            self.all_pieces[1][2][self.number_of_w_knight] = n
            self.number_of_w_knight += 1
    def bishop_creator(self,location,image,color):
        if color == "black":
            b = bishop(location,image,color,self.number_of_b_bishop)
            self.all_pieces[0][3][self.number_of_b_bishop] = b
            self.number_of_b_bishop += 1
        else:
            b = bishop(location,image,color,self.number_of_w_bishop)
            self.all_pieces[1][3][self.number_of_w_bishop] = b
            self.number_of_w_bishop += 1
    def rook_creator(self,location,image,color):
        if color == "black":
            r = rook(location,image,color,self.number_of_b_rook)
            self.all_pieces[0][4][self.number_of_b_rook] = r
            self.number_of_b_rook += 1
        else:
            r = rook(location,image,color,self.number_of_w_rook)
            self.all_pieces[1][4][self.number_of_w_rook] = r
            self.number_of_w_rook += 1
    def pawn_creator(self,location,image,color):
        if color == "black":
            p = pawn(location,image,color,self.number_of_b_pawn)
            self.all_pieces[0][5][self.number_of_b_pawn] = p
            self.number_of_b_pawn += 1
        else:
            p = pawn(location,image,color,self.number_of_w_pawn)
            self.all_pieces[1][5][self.number_of_w_pawn] = p
            self.number_of_w_pawn += 1
    def mainloop(self):
        self.master.mainloop()
    def board_creator(self):
        self.master = Tk()
        self.canvas = Canvas(self.master,height=720,width=720)
        self.canvas.pack()
        self.main_frame = Frame(self.master, highlightbackground="black", highlightthickness=3)
        self.main_frame.place(relx=1 / 7, rely=1 - 7 / 9 - 1 / 7, relwidth=7 / 9, relheight=7 / 9)
        self.left_frame = Frame(self.master, bg="gray")
        self.left_frame.place(relx=1 / 9 - 1 / 6 + 1 / 7, rely=1 - 7 / 9 - 1 / 7, relwidth=1 / 6 - 1 / 9, relheight=7 / 9)
        self.bottom_frame = Frame(self.master, bg="gray")
        self.bottom_frame.place(relx=1 / 7, rely=1 - 1 / 7, relwidth=7 / 9, relheight=1 / 6 - 1 / 9)
        for i in range(1, 9):
            label = Label(self.left_frame, text=f"{9 - i}", bg="gray", font="Arial 15 bold", fg="white")
            label.place(relheight=1 / 16, relwidth=1 / 2, rely=i * 0.125 - 1 / 11, relx=1 / 4)
        for i, value in enumerate(["A", "B", "C", "D", "E", "F", "G", "H"], 1):
            label = Label(self.bottom_frame, text=f"{value}", bg="gray", font="Arial 15 bold", fg="white")
            label.place(relheight=1 / 2, relwidth=1 / 16, rely=1 / 4, relx=i * 0.125 - 1 / 11)
        for i in range(8):
            for j in range(8):
                k = i + j
                if k % 2:
                    frame = Frame(self.main_frame, bg="#6E6A5C", highlightbackground="black", highlightthickness=0.5)
                    frame.place(relheight=1 / 8, relwidth=1 / 8, rely=i * 0.125, relx=j * 0.125)
                else:
                    frame = Frame(self.main_frame, bg="#F3DD8B", highlightbackground="black", highlightthickness=0.5)
                    frame.place(relheight=1 / 8, relwidth=1 / 8, rely=i * 0.125, relx=j * 0.125)
    def circle(self):
        square = Image.open("katana.png")
        square = square.resize((30, 30), Image.Resampling.LANCZOS)
        self.square = ImageTk.PhotoImage(square)
    def castle(self,event,location,king):
        king.move(event, location)
        if self.long_castling_b:
            rook = self.all_pieces[0][4][1]
            rook.location = [0,3]
            self.chess_board[0,0] = 0
            self.chess_board[0,3] = 140
        if self.long_castling_w:
            rook = self.all_pieces[1][4][1]
            rook.location = [7, 3]
            self.chess_board[7, 0] = 0
            self.chess_board[7, 3] = 240
        if self.short_castling_b:
            rook = self.all_pieces[0][4][0]
            rook.location = [0, 5]
            self.chess_board[0, 7] = 0
            self.chess_board[0, 5] = 141
        if self.short_castling_w:
            rook = self.all_pieces[1][4][0]
            rook.location = [7, 5]
            self.chess_board[7, 7] = 0
            self.chess_board[7, 5] = 241

        rook.bg_designer()
        rook.label.destroy()
        rook.first_move = False
        frame = Frame(self.main_frame, bg=rook.bg_color, highlightbackground="black", highlightthickness=0.5)
        frame.place(relwidth=1 / 8, relheight=1 / 8, rely=rook.location[0] * 0.125, relx=rook.location[1] * 0.125)
        rook.create()
        other_king = self.wk if rook.color == "black" else self.bk
        self.piece_calculator()
        if rook.color == "black":
            if other_king.location in [j for i in self.black_pieces for j in i.legal_moves()]:
                self.check_for_white = True
                rook.after_check_designer(other_king, "red")
        else:
            if other_king.location in [j for i in self.white_pieces for j in i.legal_moves()]:
                self.check_for_black = True
                rook.after_check_designer(other_king, "red")


        if len([j for i in self.black_pieces for j in i.legal_moves()]) == 0:
            if self.check_for_black:
                showinfo("CHECKMATE!", "White Wins!")
            else:
                showinfo("Stalemate!", "Tie!")
        elif len([j for i in self.white_pieces for j in i.legal_moves()]) == 0:
            if self.check_for_white:
                showinfo("CHECKMATE!", "Black Wins!")
            else:
                showinfo("Stalemate!", "Tie!")

        self.turn = "white" if rook.color == "black" else "black"

chess = chess_game()
chess.circle()
chess.all_piece_creator()
chess.piece_calculator()
queen_img_b = chess.bk.image_arrange("queen_b.png")
queen_img_w = chess.bk.image_arrange("queen_w.png")
knight_img_b = chess.bk.image_arrange("knight_b.png")
knight_img_w = chess.bk.image_arrange("knight_w.png")
rook_img_b = chess.bk.image_arrange("rook_b.png")
rook_img_w = chess.bk.image_arrange("rook_w.png")
bishop_img_b = chess.bk.image_arrange("bishop_b.png")
bishop_img_w = chess.bk.image_arrange("bishop_w.png")
chess.mainloop()




