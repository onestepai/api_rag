import argparse
import os

parser = argparse.ArgumentParser()


def str2bool(v):
    return v.lower() in ('true')


def add_argument_group(name):
    arg = parser.add_argument_group(name)
    return arg

# Data
data_arg = add_argument_group('Data')
data_arg.add_argument('--dataset_name', type=str, default="Weibo")
data_arg.add_argument('--train_doc', type=str, default="data/bio_data/cn/ner_T3_L300_F8_LM/train.txt")
data_arg.add_argument('--dev_doc', type=str, default="data/bio_data/cn/ner_T3_L300_F8_LM/dev.txt")
data_arg.add_argument('--test_doc', type=str, default="data/bio_data/cn/ner_T3_L300_F8_LM/dev.txt")
data_arg.add_argument('--data_stored_directory', type=str, default="data/gen_data/cn")
data_arg.add_argument('--param_stored_directory', type=str, default="models/cn/ner_T3_L300_F8_LM_model/")
data_arg.add_argument('--test_result_txt', type=str, default="data/bio_data/cn/ner_T3_L300_F8_LM/test_result")
data_arg.add_argument('--pickle_name', type=str, default="cn_list.pkl")

learn_arg = add_argument_group('Learning')
learn_arg.add_argument('--batch_size', type=int, default=8)
learn_arg.add_argument('--num_train_epochs', type=int, default=5)
learn_arg.add_argument('--max_steps', type=int, default=-1)
learn_arg.add_argument('--gradient_accumulation_steps', type=int, default=1)

learn_arg.add_argument('--learning_rate', type=float, default=3e-5)
learn_arg.add_argument('--warmup_proportion', type=float, default=0.1)
learn_arg.add_argument('--weight_decay', type=float, default=0.0)
learn_arg.add_argument("--adam_epsilon", default=1e-8, type=float, help="Epsilon for Adam optimizer.")
learn_arg.add_argument('--use_clip', type=str2bool, default=True)
learn_arg.add_argument('--max_grad_norm', type=float, default=1.0)

learn_arg.add_argument('--bert_file', type=str, default="bert-base-chinese")
learn_arg.add_argument('--bert_file_model', type=str, default="roberta_finetune_ab2/pytorch_model.bin")
learn_arg.add_argument('--bert_config', type=str, default="roberta_finetune_ab2/config.json")
learn_arg.add_argument('--bert_vocab', type=str, default="roberta_finetune_ab2/vocab.txt")
learn_arg.add_argument('--hidden_dropout_prob', type=float, default=0.2)
learn_arg.add_argument('--alpha', type=float, default=1.0)
learn_arg.add_argument('--gamma', type=float, default=2.0)

misc_arg = add_argument_group('Misc')
misc_arg.add_argument('--refresh', type=str2bool, default=False)
misc_arg.add_argument('--use_gpu', type=str2bool, default=True)
misc_arg.add_argument('--visible_gpu', type=int, default=0)
misc_arg.add_argument('--random_seed', type=int, default=1)



def get_args():

    args, unparsed = parser.parse_known_args()
    if len(unparsed) > 1:
        print("Unparsed args: {}".format(unparsed))
    return args, unparsed
