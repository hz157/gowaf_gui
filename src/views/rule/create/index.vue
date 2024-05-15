<template>
  <div class="container">
    <Breadcrumb :items="['menu.rule', 'menu.rule.create']" />
    <a-spin :loading="loading" style="width: 100%">
      <a-card class="general-card">
        <template #title>
          {{ $t('menu.rule.create.title') }}
        </template>
        <div class="wrapper">
          <a-form
            ref="formRef"
            :model="submitModel"
            :label-col-props="{ span: 6 }"
            :wrapper-col-props="{ span: 18 }"
            class="form"
            @submit="submitForm"
          >
            <a-form-item
              field="RuleName"
              :label="$t('rule.create.form.label.ruleName')"
              :rules="[
                {
                  required: true,
                  message: $t('rule.create.form.label.ruleName.required'),
                },
              ]"
            >
              <a-input
                v-model="submitModel.RuleName"
                :placeholder="$t('rule.create.form.label.ruleName.required')"
              />
            </a-form-item>
            <a-form-item
              field="RuleDesc"
              :label="$t('rule.create.form.label.ruleDesc')"
              :rules="[
                {
                  required: true,
                  message: $t('rule.create.form.label.ruleDesc.required'),
                },
              ]"
            >
              <a-input
                v-model="submitModel.RuleDesc"
                :placeholder="$t('rule.create.form.label.ruleDesc.required')"
              />
            </a-form-item>
            <a-form-item
              field="RuleReg"
              :label="$t('rule.create.form.label.ruleReg')"
              :rules="[
                {
                  required: true,
                  message: $t('rule.create.form.label.ruleReg.required'),
                },
              ]"
            >
              <a-input
                v-model="submitModel.RuleReg"
                :placeholder="$t('rule.create.form.label.ruleReg.required')"
              />
            </a-form-item>
            <a-form-item
              field="ruleMatch"
              :label="$t('rule.create.form.label.ruleMatch')"
              :rules="[
                {
                  required: true,
                  message: $t('rule.create.form.label.ruleMatch.required'),
                },
              ]"
            >
              <a-select
                v-model="submitModel.ruleMatch"
                :placeholder="$t('rule.create.form.placeholder.ruleMatch')"
              >
                <a-option>Body</a-option>
                <a-option>Url</a-option>
                <a-option>User-Agent</a-option>
              </a-select>
            </a-form-item>
            <div class="form-actions">
              <a-button type="primary" html-type="submit">{{
                $t('rule.create.form.submit')
              }}</a-button>
            </div>
          </a-form>
        </div>
      </a-card>
    </a-spin>
  </div>
</template>

<script lang="ts" setup>
  import { ref } from 'vue';
  import useLoading from '@/hooks/loading';
  import { AddRuleStr, AddRule } from '@/api/rule';
  import { useRouter } from 'vue-router';
  import { FormInstance } from '@arco-design/web-vue/es/form';

  const router = useRouter();

  interface RuleFormModel {
    RuleName: string;
    RuleDesc: string;
    RuleReg: string;
    ruleMatch: string;
  }

  const { loading, setLoading } = useLoading(false);
  const formRef = ref<FormInstance>();
  const submitModel = ref<RuleFormModel>({
    RuleName: '',
    RuleDesc: '',
    RuleReg: '',
    ruleMatch: '',
  });

  const submitForm = async () => {
    const res = await formRef.value?.validate();
    if (!res) {
      setLoading(true);
      try {
        const addRuleData: AddRuleStr = {
          name: submitModel.value.RuleName,
          desc: submitModel.value.RuleDesc,
          reg: submitModel.value.RuleReg,
          field: submitModel.value.ruleMatch,
        };
        const response = await AddRule(addRuleData);
        console.log('AddRule response:', response);
        submitModel.value = {
          RuleName: '',
          RuleDesc: '',
          RuleReg: '',
          ruleMatch: '',
        }; // 重置表单
      } catch (err) {
        // 错误处理
      } finally {
        router.push('/rule/manage');
        setLoading(false);
      }
    }
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px 20px;
  }
  .wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 64px 0;
    background-color: var(--color-bg-2);
    :deep(.arco-form) {
      .arco-form-item {
        &:last-child {
          margin-top: 20px;
        }
      }
    }
  }
  .form-actions {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
  .form {
    width: 500px;
  }
</style>
