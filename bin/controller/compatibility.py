import sys

if '../' not in sys.path:
    sys.path.append('../')  # 同階層の読み込みに必須
import settings.constant

class Compatibility:
    msg = '"/相性, タイプ, タイプ(単タイプなら省略)" でタイプ相性を教えてあげるよ～！ (ーqー)'
    def __init__(self):
        self.compatibility_df = settings.constant.COMPATIBILITY_DF
    
    def get_compatibility_msg(self, types):
        '''
        引数typesに含まれる属性に応じて, 被ダメージ時と与ダメージ時の得意不得意属性メッセージをStringで返す.
        引数: 
            types: List
        返り値: 
            msg: String
        '''
        
        if len(types) == 2:
            if types[1] in settings.constant.types:
                attack_compatibility_ser = self.compatibility_df.loc[types[1]]
                attack_compatibility_type_and_magnification = [[c, ct] for (c, ct) in zip(attack_compatibility_ser, attack_compatibility_ser.index) if c != 1]
                diffence_compatibility_ser = self.compatibility_df.loc[:, types[1]]
                diffence_compatibility_type_and_magnification = [[c, ct] for (c, ct) in zip(diffence_compatibility_ser, diffence_compatibility_ser.index) if c != 1]
                atk_no_effect, bad_list, atk_not_good, atk_good, atk_great_list= self.sort_by_compatibility(attack_compatibility_type_and_magnification)
                dif_perfect, dif_good, dif_not_bad, dif_not_good, dif_bad= self.sort_by_compatibility(diffence_compatibility_type_and_magnification)
                if atk_no_effect == []:
                    msg = f'{types[1]}の攻撃は, {atk_good}が得意で {atk_not_good}が苦手だよ! \n 攻撃を受ける時, {dif_good}が得意で {dif_bad}が苦手, {dif_perfect}は全く効かないよ!(ーqー)'
                elif dif_perfect == []:
                    msg = f'{types[1]}の攻撃は, {atk_good}が得意で {atk_not_good}が苦手, {atk_no_effect}は全く効かないよ! \n 攻撃を受ける時, {dif_good}が得意で {dif_bad}が苦手だよ!(ーqー)'
                else:
                    msg = f'{types[1]}の攻撃は, {atk_good}が得意で {atk_not_good}が苦手, {atk_no_effect}は全く効かないよ! \n 攻撃を受ける時, {dif_good}が得意で {dif_bad}が苦手, {dif_perfect[0]}は全く効かないよ!(ーqー)'
            else:
                msg = f'次の中からひらがなで入力してね(ーqー) {settings.constant.types}'

        elif len(types) == 3:
            if types[1] in settings.constant.types and types[2] in settings.constant.types:
                atk1_good_msg, atk2_good_msg = ["", ""]
                atk1_not_good_msg, atk2_not_good_msg = ["", ""]
                bad_msg1, bad_msg2 = ["", ""]
                good_msg1, good_msg2 = ["", ""]
                type1 = types[1]
                type2 = types[2]
                attack_compatibility_ser1 = self.compatibility_df.loc[type1]
                attack_compatibility_type_and_magnification1 = [[c, ct] for (c, ct) in zip(attack_compatibility_ser1, attack_compatibility_ser1.index) if c != 1]
                attack_compatibility_ser2 = self.compatibility_df.loc[type2]
                attack_compatibility_type_and_magnification2 = [[c, ct] for (c, ct) in zip(attack_compatibility_ser2, attack_compatibility_ser2.index) if c != 1]
                multiplied_diffence_compatibility = self.compatibility_df.loc[:,type1] * self.compatibility_df.loc[:,type2]
                diffence_compatibility_type_and_magnification = [[c, ct] for (c, ct) in zip(multiplied_diffence_compatibility, multiplied_diffence_compatibility.index) if c != 1]
                atk1_no_effect, atk1_bad, atk1_not_good, atk1_good, atk1_great= self.sort_by_compatibility(attack_compatibility_type_and_magnification1)
                atk2_no_effect, atk2_bad, atk2_not_good, atk2_good, atk2_great= self.sort_by_compatibility(attack_compatibility_type_and_magnification2)
                # no_effect_list, bad_list, not_good_list, good_list, great_list
                dif_perfect, dif_good, dif_not_bad, dif_not_good, dif_bad= self.sort_by_compatibility(diffence_compatibility_type_and_magnification)
                if len(atk1_good) >= 1:
                    atk1_good_msg = "が得意で"
                if len(atk2_good) >= 1:
                    atk2_good_msg = "が得意で"
                if len(atk1_not_good) >= 1:
                    atk1_not_good_msg = "が苦手"
                if len(atk2_not_good) >= 1:
                    atk2_not_good_msg = "が苦手"
                if len(dif_bad) >= 1:
                    bad_msg1 = " 特に"
                    bad_msg2 = "はめちゃくちゃ苦手"
                if len(dif_good) >= 1:
                    good_msg1 = " 特に"
                    good_msg2 = "はめちゃくちゃ得意"
                
                if atk1_no_effect == [] and atk2_no_effect == [] and dif_perfect == []:
                    msg = f'{type1}の攻撃は, {atk1_good if atk1_good != [] else ""}{atk1_good_msg} {atk1_not_good if atk1_not_good != [] else ""}{atk1_not_good_msg}だよ!\n \
{type2}の攻撃は, {atk2_good if atk2_good != [] else ""}{atk2_good_msg} {atk2_not_good if atk2_not_good != [] else ""}{atk2_not_good_msg}だよ!\n  \
攻撃を受ける時は, {dif_not_bad}{dif_good if dif_good != [] else ""}が得意で{good_msg1}{dif_good if dif_good != [] else ""}{good_msg2}, {dif_not_good}{dif_bad if dif_bad != [] else ""}が苦手{bad_msg1}{dif_bad if dif_bad != [] else ""}{bad_msg2}だよ！(ーqー)'            
                elif atk1_no_effect == [] and atk2_no_effect == []:
                    msg = f'{type1}の攻撃は, {atk1_good if atk1_good != [] else ""}{atk1_good_msg} {atk1_not_good if atk1_not_good != [] else ""}{atk1_not_good_msg}だよ!\n \
{type2}の攻撃は, {atk2_good if atk2_good != [] else ""}{atk2_good_msg} {atk2_not_good if atk2_not_good != [] else ""}{atk2_not_good_msg}だよ!\n  \
攻撃を受ける時は, {dif_not_bad}{dif_good if dif_good != [] else ""}が得意で{good_msg1}{dif_good if dif_good != [] else ""}{good_msg2}, {dif_not_good}{dif_bad if dif_bad != [] else ""}が苦手{bad_msg1}{dif_bad if dif_bad != [] else ""}{bad_msg2}, {dif_perfect}は全く効かないよ!(ーqー)'
                elif atk1_no_effect == [] and dif_perfect == []:
                    msg = f'{type1}の攻撃は, {atk1_good if atk1_good != [] else ""}{atk1_good_msg} {atk1_not_good if atk1_not_good != [] else ""}{atk1_not_good_msg}だよ!\n \
{type2}の攻撃は, {atk2_good if atk2_good != [] else ""}{atk2_good_msg} {atk2_not_good if atk2_not_good != [] else ""}{atk2_not_good_msg}, {atk2_no_effect}は全く効かないよ!\n \
攻撃を受ける時は, {dif_not_bad}{dif_good if dif_good != [] else ""}が得意で{good_msg1}{dif_good if dif_good != [] else ""}{good_msg2}, {dif_not_good}{dif_bad if dif_bad != [] else ""}が苦手{bad_msg1}{dif_bad if dif_bad != [] else ""}{bad_msg2}だよ！(ーqー)'
                elif atk1_no_effect == []:
                    msg = f'{type1}の攻撃は, {atk1_good if atk1_good != [] else ""}{atk1_good_msg} {atk1_not_good if atk1_not_good != [] else ""}{atk1_not_good_msg}だよ!\n \
{type2}の攻撃は, {atk2_good if atk2_good != [] else ""}{atk2_good_msg} {atk2_not_good if atk2_not_good != [] else ""}{atk2_not_good_msg}, {atk2_no_effect}は全く効かないよ!\n \
攻撃を受ける時は, {dif_not_bad}{dif_good if dif_good != [] else ""}が得意で{good_msg1}{dif_good if dif_good != [] else ""}{good_msg2}, {dif_not_good}{dif_bad if dif_bad != [] else ""}が苦手{bad_msg1}{dif_bad if dif_bad != [] else ""}{bad_msg2}, {dif_perfect}は全く効かないよ!(ーqー)'
                elif atk2_no_effect == [] and dif_perfect == []:
                    msg = f'{type1}の攻撃は, {atk1_good if atk1_good != [] else ""}{atk1_good_msg} {atk1_not_good if atk1_not_good != [] else ""}{atk1_not_good_msg}, {atk1_no_effect}は全く効かないよ!\n \
{type2}の攻撃は, {atk2_good if atk2_good != [] else ""}{atk2_good_msg} {atk2_not_good if atk2_not_good != [] else ""}{atk2_not_good_msg}だよ!\n  \
攻撃を受ける時は, {dif_not_bad}{dif_good if dif_good != [] else ""}が得意で{good_msg1}{dif_good if dif_good != [] else ""}{good_msg2}, {dif_not_good}{dif_bad if dif_bad != [] else ""}が苦手{bad_msg1}{dif_bad if dif_bad != [] else ""}{bad_msg2}だよ！(ーqー)'
                elif atk2_no_effect == []:
                    msg = f'{type1}の攻撃は, {atk1_good if atk1_good != [] else ""}{atk1_good_msg} {atk1_not_good if atk1_not_good != [] else ""}{atk1_not_good_msg}, {atk1_no_effect}は全く効かないよ!\n \
{type2}の攻撃は, {atk2_good if atk2_good != [] else ""}{atk2_good_msg} {atk2_not_good if atk2_not_good != [] else ""}{atk2_not_good_msg}だよ!\n  \
攻撃を受ける時は, {dif_not_bad}{dif_good if dif_good != [] else ""}が得意で{good_msg1}{dif_good if dif_good != [] else ""}{good_msg2}, {dif_not_good}{dif_bad if dif_bad != [] else ""}が苦手{bad_msg1}{dif_bad if dif_bad != [] else ""}{bad_msg2}, {dif_perfect}は全く効かないよ!(ーqー)'
                elif dif_perfect == []:
                    msg = f'{type1}の攻撃は, {atk1_good if atk1_good != [] else ""}{atk1_good_msg} {atk1_not_good if atk1_not_good != [] else ""}{atk1_not_good_msg}, {atk1_no_effect[0]}は全く効かないよ!\n \
{type2}の攻撃は, {atk2_good if atk2_good != [] else ""}{atk2_good_msg} {atk2_not_good if atk2_not_good != [] else ""}{atk2_not_good_msg}, {atk2_no_effect}は全く効かないよ!\n  \
攻撃を受ける時は, {dif_not_bad}{dif_good if dif_good != [] else ""}が得意で{good_msg1}{dif_good if dif_good != [] else ""}{good_msg2}, {dif_not_good}{dif_bad if dif_bad != [] else ""}が苦手{bad_msg1}{dif_bad if dif_bad != [] else ""}{bad_msg2}だよ！(ーqー)' 
                else:
                    msg = f'{type1}の攻撃は, {atk1_good if atk1_good != [] else ""}{atk1_good_msg} {atk1_not_good if atk1_not_good != [] else ""}{atk1_not_good_msg}, {atk1_no_effect}は全く効かないよ!\n \
{type2}の攻撃は, {atk2_good if atk2_good != [] else ""}{atk2_good_msg} {atk2_not_good if atk2_not_good != [] else ""}{atk2_not_good_msg}, {atk2_no_effect}は全く効かないよ!\n \
攻撃を受ける時は, {dif_not_bad}{dif_good if dif_good != [] else ""}が得意で{good_msg1}{dif_good if dif_good != [] else ""}{good_msg2}, {dif_not_good}{dif_bad if dif_bad != [] else ""}が苦手{bad_msg1}{dif_bad if dif_bad != [] else ""}{bad_msg2}, {dif_perfect}は全く効かないよ!(ーqー)' 
            else:
                msg = f'次の中からひらがなで入力してね(ーqー) {settings.constant.types}'

        else:
            msg = '3つ以上タイプが入力されてるよ～ (ーqー)'

        return msg

    def sort_by_compatibility(self, multiple_list):
        '''
        引数multiple_listに含まれる倍率に応じて, 得意不得意属性をList[String]で返す.
        引数: 
            multiple_list: List[List]
        返り値: 
            msg: List[String]
        '''
        no_effect_list = []
        bad_list =[]
        not_good_list = []
        good_list = []
        great_list = []
        for list in multiple_list:
            if list[0] == 0:
                no_effect_list.append(list[1])
            elif list[0] == 0.25:
                bad_list.append(list[1])
            elif list[0] == 0.5:
                not_good_list.append(list[1])
            elif list[0] == 2:
                good_list.append(list[1])
            elif list[0] ==4:
                great_list.append(list[1])

        return no_effect_list, bad_list, not_good_list, good_list, great_list

