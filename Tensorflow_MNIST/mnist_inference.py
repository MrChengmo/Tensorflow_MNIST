# -*- coding: utf-8 -*-
import tensorflow as tf

#定义神经网络相关参数
INPUT_NODE = 784
OUTPUT_NODE = 10
LAYER1_NODE = 500

#通过tf.get_variable函数来获取变量。在神经网络训练时会创建这些变量；在测试时会通过保存的模型加载这些变量的取值。
#可以再变量加载时将滑动平均变量重命名，所以可以直接通过同样的名字在训练时使用变量自身，而在测试时使用变量的滑动平均值。
#在这个函数中也会将变量的正则化损失加入损失集合
def get_weight_variable(shape,regularizer):
    weights = tf.get_variable("weights",shape,initializer=tf.truncated_normal_initializer(stddev=0.1))

  #当给出了正则化生成函数时，将当前变量的正则化损失加入名字为losses的集合。
  #此处使用add_to_collection函数将一个张量加入一个集合，而这个集合的名称为losses
  #这是自定义集合，不在tensorflow自动管理的集合列表中
    if regularizer != None:
        tf.add_to_collection('losses',regularizer(weights))
    return weights

#定义神经网络的前向传播过程
def inference(input_tensor,regularizer):
    #声明第一层网络的变量并完成前向传播
    with tf.variable_scope('layer1'):
        weights = get_weight_variable(
            [INPUT_NODE,LAYER1_NODE],regularizer)
        biases = tf.get_variable(
            "biases",[LAYER1_NODE],
            initializer = tf.constant_initializer(0.0))
        layer1 = tf.nn.relu(tf.matmul(input_tensor,weights)+biases)

    #声明第二层网络的变量并完成前向传播
    with tf.variable_scope('layer2'):
        weights = get_weight_variable(
            [LAYER1_NODE,OUTPUT_NODE],regularizer)
        biases = tf.get_variable(
            "biases",[OUTPUT_NODE],
            initializer = tf.constant_initializer(0.0))
        layer2 = tf.matmul(layer1,weights)+biases
    return layer2   